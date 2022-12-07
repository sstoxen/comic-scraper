from datetime import date

from ..ComicScraper import ComicScraper
from ..GoComicsScraper import GoComicsScraper


class BusinessCatScraper(ComicScraper):
    def __init__(self):
        self._scraper = GoComicsScraper(
            "The Adventures of Business Cat", "the-adventures-of-business-cat")

    def get_all_comics(self):
        skip_dates = (
            date(2015, 12, 28),
            date(2016, 1, 4),
            date(2017, 1, 30)
        )
        self._scraper.get_all_comics_in_range(
            date(2015, 4, 27), date(2018, 11, 12), interval=7, skip_dates=skip_dates)
