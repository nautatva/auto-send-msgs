import enum


@enum.unique
class Frequency(str, enum.Enum):
    ONCE = None
    DAILY = "1D"
    WEEKLY = "7D"
    MONTHLY = "1M"
    YEARLY = "1Y"

    @classmethod
    def choices(cls):
        return [(item.value, item.name.title()) for item in cls]
