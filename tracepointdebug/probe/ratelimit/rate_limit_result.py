from enum import Enum


class RateLimitResult(Enum):
    OK = "OK"
    HIT = "HIT"
    EXCEEDED = "EXCEEDED"
