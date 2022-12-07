from datetime import date

from ..GoComicsScraper import GoComicsScraper


class CalvinAndHobbesScraper():
    def __init__(self):
        self._scraper = GoComicsScraper(
            "Calvin and Hobbes", "calvinandhobbes")

    def get_all_comics(self):
        self._scraper.get_all_comics_in_range(
            date(1985, 11, 18), date(1995, 12, 31))
