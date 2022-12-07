from datetime import date

from .. import GoComicsScraper, ComicScraper


class OverTheHedgeScraper(ComicScraper):
    def __init__(self):
        self._scraper = GoComicsScraper(
            "Over the Hedge", "overthehedge")

    def get_all_comics(self):
        skip_days_of_the_week = [6]
        skip_dates_1996 = (
            date(1996, 10, 7),
            date(1996, 10, 8),
            date(1996, 10, 9),
            date(1996, 10, 10),
            date(1996, 10, 11),
            date(1996, 10, 12)
        )
        skip_dates_1999 = (
            date(1999, 7, 26),
            date(1999, 7, 27),
            date(1999, 7, 28),
            date(1999, 7, 29),
            date(1999, 7, 30),
            date(1999, 7, 31)
        )
        skip_dates_2003 = (
            date(2003, 11, 17),
        )
        skip_dates_2008 = (
            date(2008, 9, 5),
        )
        skip_dates1 = (*skip_dates_1999, *skip_dates_2003, *skip_dates_2008)
        self._scraper.get_all_comics_in_range(
            date(1995, 6, 12), date(1995, 7, 22), skip_days_of_the_week=skip_days_of_the_week)
        self._scraper.get_all_comics_in_range(
            date(1996, 1, 29), date(1996, 11, 30), skip_dates=skip_dates_1996, skip_days_of_the_week=skip_days_of_the_week)
        self._scraper.get_all_comics_in_range(
            date(1997, 1, 1), date(2011, 2, 26), skip_dates=skip_dates1, skip_days_of_the_week=skip_days_of_the_week)
        self._scraper.get_all_comics_in_range(
            date(2011, 4, 29), date(2011, 5, 28), skip_days_of_the_week=skip_days_of_the_week)
        # Start a new run with the date where it went to 7 days a week.
        self._scraper.get_all_comics_in_range(date(2011, 5, 31), date.today())
