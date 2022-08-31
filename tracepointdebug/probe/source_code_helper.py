import hashlib
from functools import wraps

import six
from tracepointdebug.utils import debug_logger


def memoize(function):
    memo = {}

    @wraps(function)
    def wrapper(*args):
        try:
            return memo[args]
        except KeyError:
            rv = function(*args)
            memo[args] = rv
            return rv

    return wrapper


def get_source_code(file_path):
    if file_path is None or file_path.endswith('.pyc'):
        return None
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
            return file_content
    except IOError as e:
        debug_logger('Error reading file from file path: ' + file_path + ' err:', e)
    return None


@memoize
def get_source_code_hash(file_path):
    source_code = get_source_code(file_path)
    if source_code is None:
        return None

    if six.PY2:
        source_code = source_code.replace('\r\n', '\n') \
            .replace('\r\x00\n\x00', '\n\x00') \
            .replace('\r', '\n')
    else:
        source_code = source_code.decode().replace('\r\n', '\n') \
            .replace('\r\x00\n\x00', '\n\x00') \
            .replace('\r', '\n').encode('UTF8')

    try:
        source_hash = hashlib.sha256(source_code).hexdigest()
        return source_hash
    except Exception as e:
        debug_logger('Unable to calculate hash of source code from file %s error: %s' % (file_path, e))

    return None
