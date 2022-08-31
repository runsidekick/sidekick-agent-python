from threading import Lock

from tracepointdebug.probe.ratelimit.rate_limit_result import RateLimitResult

SECONDS_IN_MINUTE = 60
RATE_LIMIT_WINDOW = 4
RATE_LIMIT_IDX_MASK = RATE_LIMIT_WINDOW - 1
LIMIT_IN_MINUTE = 1000


class RateLimitInfo(object):
    def __init__(self, minute):
        self._lock = Lock()
        self.minute = minute
        self.count = 0

    def increment_and_get(self):
        with self._lock:
            self.count += 1
            count = self.count
        return count


class RateLimiter(object):
    def __init__(self):
        self._lock = Lock()
        self.rate_limit_infos = [None] * RATE_LIMIT_WINDOW

    def check_rate_limit(self, current_time):
        current_min = int(current_time / SECONDS_IN_MINUTE)
        rate_limit_info_idx = current_min & RATE_LIMIT_IDX_MASK
        with self._lock:
            rate_limit_info = self.rate_limit_infos[rate_limit_info_idx]
            if rate_limit_info is None or rate_limit_info.minute < current_min:
                rate_limit_info = RateLimitInfo(current_min)
                self.rate_limit_infos[rate_limit_info_idx] = rate_limit_info
            elif rate_limit_info.minute > current_min:
                return RateLimitResult.OK

            count = rate_limit_info.increment_and_get()
            if count < LIMIT_IN_MINUTE:
                return RateLimitResult.OK
            elif count == LIMIT_IN_MINUTE:
                return RateLimitResult.HIT
            else:
                return RateLimitResult.EXCEEDED


