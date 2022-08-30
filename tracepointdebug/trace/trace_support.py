from inspect import trace
import logging
from .trace_context import TraceContext
logger = logging.getLogger(__name__)

class TraceSupport:
    
    TRACEPOINT_SNAPSHOT_EXIST_TAG = "tracepoint.snapshot.exist"
    THUNDRA_CHECK_DISABLED = False
    OPENTRACING_CHECK_DISABLED = False

    @classmethod
    def get_trace_context(cls):
        trace_context = cls.get_trace_context_from_thundra()
        if not trace_context:
            trace_context = cls.get_trace_context_from_opentracing()
        return trace_context

    @classmethod
    def get_trace_context_from_thundra(cls):
        if cls.THUNDRA_CHECK_DISABLED:
            return 
        try:
            from thundra.opentracing.tracer import ThundraTracer
            from thundra.plugins.invocation import invocation_support
            active_span = ThundraTracer.get_instance().get_active_span()
            if active_span:
                invocation_support.set_agent_tag(cls.TRACEPOINT_SNAPSHOT_EXIST_TAG, True)
                return TraceContext(
                    trace_id=active_span.trace_id,
                    transaction_id=active_span.transaction_id,
                    span_id=active_span.span_id)
        except (ImportError, AttributeError) as error:
            cls.THUNDRA_CHECK_DISABLED = True
        except Exception as e:
            logger.debug("Unable to get trace context from Thundra: {0}".format(e))
        return

    @classmethod
    def get_trace_context_from_opentracing(cls):
        if cls.OPENTRACING_CHECK_DISABLED:
            return 
        try:
            import opentracing
            tracer = opentracing.global_tracer()
            if tracer:
                span = tracer.active_span
                if span:
                    span_context = span.context
                    if span_context:
                        return TraceContext(
                            trace_id=span_context.trace_id,
                            transaction_id=None,
                            span_id=span_context.span_id)
        except (ImportError, AttributeError) as error:
            cls.OPENTRACING_CHECK_DISABLED = True
        except Exception as e:
            logger.debug("Unable to get trace context from Opentracing: {0}".format(e))
        return