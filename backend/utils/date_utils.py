from choices.time import Frequency
from datetime import date, timedelta


def get_nearest_date(get_date_around:date, ref_date:date, frequency:Frequency) -> date:
    """
        Returns date just before or equal to get_date_around.
    """
    if frequency == Frequency.ONCE:
        return ref_date
    if frequency == Frequency.DAILY:
        return get_date_around
    if frequency == Frequency.WEEKLY:
        no_of_weeks = (get_date_around - ref_date).days / 7
        whole_days = int(no_of_weeks) * 7
        return get_date_around + timedelta(days=whole_days)
    if frequency == Frequency.MONTHLY:
        new_date = get_date_around.replace(month=ref_date.month, year=ref_date.year)
        return new_date
    if frequency == Frequency.YEARLY:
        new_date = get_date_around.replace(year=ref_date.year)
        return new_date


def is_event_valid_at_reference_date(date_to_check:date, ref_date:date, frequency:Frequency) -> bool:
    nearest_freq_date = get_nearest_date(date_to_check, ref_date, frequency)
    if nearest_freq_date == date_to_check:
        return True
    return False
