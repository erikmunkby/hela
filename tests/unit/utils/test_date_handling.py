import pytest
from datetime import date
from hela._utils.date_utils import get_date_range_from_set, get_missing_dates


@pytest.mark.base
def test_date_range_building():
    dates = {date(2021, 4, 1), date(2021, 4, 3), date(2021, 4, 5)}
    assert len(get_date_range_from_set(dates)) == 5

    assert get_date_range_from_set(dates) == {
        date(2021, 4, 1), date(2021, 4, 2), date(2021, 4, 3), date(2021, 4, 4),
        date(2021, 4, 5)
    }


@pytest.mark.base
def test_missing_dates():
    dates = {date(2021, 4, 1), date(2021, 4, 3), date(2021, 4, 5)}

    assert len(get_missing_dates(dates)) == 2

    assert get_missing_dates(dates) == {date(2021, 4, 2), date(2021, 4, 4)}
