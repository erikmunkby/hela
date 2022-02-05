from datetime import date, timedelta
from catalog.plots.date_plots import plot_date_availability_calendar


def test_date_plots():
    """This test will only make sure it executes, for visual tests run in notebook."""
    dates = [date(2021, 1, 1) + timedelta(days=x) for x in range(100)]
    dates.pop(3)
    dates.pop(12)
    plot_date_availability_calendar(dates)
