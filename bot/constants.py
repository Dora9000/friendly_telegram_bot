from enum import Enum

INIT_K = 0.2
GRAD_K = 0.8


class StatusEnum(Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
