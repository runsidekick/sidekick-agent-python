import json
from tracepointdebug.utils import debug_logger

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
            debug_logger(e)


def to_json(data, separators=None):
    return json.dumps(data, separators=separators, cls=JSONEncoder)
