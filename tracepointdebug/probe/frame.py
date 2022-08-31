class Frame(object):
    def __init__(self, line_no, variables, path, method_name):
        self.line_no = line_no
        self.variables = variables
        self.path = path
        self.method_name = method_name

    def __repr__(self):
        return str({
            "line": self.line_no,
            "locals": self.variables,
            "path": self.path,
            "methodName": self.method_name,
        })

    def to_json(self):
        return {
            "lineNo": self.line_no,
            "variables": self.variables,
            "fileName": self.path,
            "methodName": self.method_name
        }
