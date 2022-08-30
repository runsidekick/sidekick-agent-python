class CodedError:
    def __init__(self, code, msg_template):
        self.code = code
        self.msg_template = msg_template

    def format_message(self, args):
        return self.msg_template.format(*args)
