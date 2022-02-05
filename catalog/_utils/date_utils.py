from datetime import date, timedelta
from typing import Set


def get_date_range_from_set(dates: Set[date]) -> Set[date]:
    """
        Returns an inclusive set range with all available dates between max and min of input dates.

        Args:
            dates: A set of dates e.g. {date(2020, 1, 1), date(202, 1, 3)}

        Returns:
            An inclusive set of dates [min_date, max_date]
    """
    min_date, max_date = min(dates), max(dates)
    return {min_date + timedelta(days=x) for x in range((max_date - min_date).days + 1)}


def get_missing_dates(dates: Set[date]) -> Set[date]:
    """
        Returns dates missing from dataset as a set of dates.
        Requires .get_dates() to be implemented.

        Returns:
            Set of missing dates
    """
    return get_date_range_from_set(dates) - dates
