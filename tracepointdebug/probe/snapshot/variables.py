class Variables(object):
    def __init__(self, variables):
        self.variables = variables

    def to_json(self):
        return {var.name: var.value for var in self.variables}
