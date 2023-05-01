import enum


class MQEventType(str, enum.Enum):
    change = "event.change"
    complete = "event.complete"
    delete = "event.delete"
