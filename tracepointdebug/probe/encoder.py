import json


class JSONEncoder(json.JSONEncoder):
    def default(self, z):
        try:
            if "to_json" in dir(z):
                return z.to_json()
            elif isinstance(z, bytes):
                return z.decode('utf-8', errors='ignore')
            else:
                return super(JSONEncoder, self).default(z)
        except Exception as e:
            print(e)


def to_json(data, separators=None):
    return json.dumps(data, separators=separators, cls=JSONEncoder)
