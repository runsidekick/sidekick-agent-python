import abc

from tracepointdebug.probe.breakpoints.tracepoint import TracePointManager
from tracepointdebug.probe.breakpoints.logpoint import LogPointManager
from tracepointdebug.broker.application.application_status_provider import ApplicationStatusProvider

ABC = abc.ABCMeta('ABC', (object,), {})


class ApplicationStatusTracePointProvider(ApplicationStatusProvider):

    def provide(self, application_status, client=None):
        application_status.trace_points = TracePointManager.instance().list_trace_points(client)
        application_status.log_points = LogPointManager.instance().list_log_points(client)
