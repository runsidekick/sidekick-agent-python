from tracepointdebug.probe.condition.value_provider import ValueProvider


class VariableValueProvider(ValueProvider):

    def __init__(self, var_name):
        self.var_name = var_name

    def get_value(self, condition_context):
        return condition_context.get_variable_value(self.var_name)
