import enum


class EventStatus(enum.Enum):
    deleted = "Удалено"
    planned = "Запланировано"
    completed = "Завершено"
    underway = "Идет"
