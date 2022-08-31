class TraceContext:

    def __init__(self, trace_id=None, transaction_id=None, span_id=None):
        self.trace_id = trace_id
        self.transaction_id = transaction_id
        self.span_id = span_id 

    def get_trace_id(self):
        return self.trace_id

    def get_transaction_id(self):
        return self.transaction_id

    def get_span_id(self):
        return self.span_id