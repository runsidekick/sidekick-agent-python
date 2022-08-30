class CodedException(Exception):
    def __init__(self, coded_error, args):
        super(CodedException, self).__init__(coded_error.format_message(args))
        self.code = coded_error.code
