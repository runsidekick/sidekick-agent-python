class LogPointConfig(object):

    def __init__(self, log_point_id, file=None, file_ref=None, line=None, client=None, log_expression=None, cond=None, expire_duration=None, expire_hit_count=None,
                 file_hash=None, disabled=False, log_level="INFO", stdout_enabled=False, tags=set()):
        self.log_point_id = log_point_id
        self.file = file
        self.file_ref = file_ref
        self.file_hash = file_hash
        self.line = line
        self.client = client
        self.cond = cond
        self.expire_duration = expire_duration
        self.expire_hit_count = expire_hit_count
        self.disabled = disabled
        self.log_expression = log_expression
        self.log_level = log_level
        self.stdout_enabled = stdout_enabled
        self.tags = tags

    def get_file_name(self):
        return self.file if not self.file_ref else '{0}?ref={1}'.format(self.file, self.file_ref)

    def to_json(self):
        return {
            "id": self.log_point_id,
            "fileName": self.get_file_name(),
            "lineNo": self.line,
            "expireSecs": self.expire_duration,
            "client": self.client,
            "expireCount": self.expire_hit_count,
            "disabled": self.disabled,
            "logExpression": self.log_expression,
            "logLevel": self.log_level,
            "stdoutEnabled": self.stdout_enabled,
            "conditionExpression": self.cond,
            "tags": list(self.tags)
        }
