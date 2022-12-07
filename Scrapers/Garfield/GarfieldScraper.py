from datetime import date

from ..GoComicsScraper import GoComicsScraper
from ..ComicScraper import ComicScraper


class GarfieldScraper(ComicScraper):
    def __init__(self):
        self._scraper = GoComicsScraper(
            "Garfield", "garfield")

    def get_all_comics(self):
        self._scraper.get_all_comics_in_range(
            date(1978, 6, 19), date.today())
