class ApplicationStatus(object):

    def __init__(self, instance_id=None, name=None, stage=None, version=None, ip=None, hostname=None,
                 trace_points=None, log_points=None, runtime=None):
        self.instance_id = instance_id
        self.name = name
        self.stage = stage
        self.version = version
        self.ip = ip
        self.hostname = hostname
        self.trace_points = trace_points
        if self.trace_points is None:
            self.trace_points = []
        self.log_points = log_points
        if self.log_points is None:
            self.log_points = []
        self.runtime = runtime

    def to_json(self):
        return {
            "name": self.name,
            "instanceId": self.instance_id,
            "stage": self.stage,
            "version": self.version,
            "ip": self.ip,
            "hostName": self.hostname,
            "tracePoints": self.trace_points,
            "logPoints": self.log_points,
            "runtime": self.runtime
        }
