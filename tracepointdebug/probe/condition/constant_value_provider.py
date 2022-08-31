from tracepointdebug.probe.condition.value_provider import ValueProvider


class ConstantValueProvider(ValueProvider):

    def __init__(self, value):
        self.value = value

    def get_value(self, condition_context):
        return self.value
