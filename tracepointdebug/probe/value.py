class Value(object):
    def __init__(self, var_type, value):
        self.type = var_type
        self.value = value

    def __repr__(self):
        return str(
            self.value
        )

    def to_json(self):
        return {
            "@type": str(self.type),
            "@value": self.value
        }
