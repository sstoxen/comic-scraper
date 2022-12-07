from abc import ABC, abstractmethod


class ComicScraper(ABC):
    @abstractmethod
    def get_all_comics(self):
        pass
