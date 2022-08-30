class Variable(object):
    def __init__(self, name, var_type, value):
        self.name = name
        self.type = var_type
        self.value = value

    def __repr__(self):
        return str(
            {
                "name": self.name,
                "type": self.type,
                "value": self.value
            }
        )

    def to_json(self):
        return {
            "@type": str(self.type),
            "@value": self.value
        }
