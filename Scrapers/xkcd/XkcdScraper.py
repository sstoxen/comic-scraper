from typing import Tuple
import requests
import os
from time import sleep
# from html.parser import HTMLParser
from bs4 import BeautifulSoup

from Logger.Logger import Logger
from ..ComicScraper import ComicScraper

"""
So many outliers...

Interesting Skippers:
- 1331 is a table of gifs showing the frequency of different events. Not sure how to deal with this one.
- 1350 is a choose your own adventure.
- 1416 is an infinite (?) zoom.
- 1525 is a magic 8 ball.
- 1608 is a platform game.
- 1663 is some .js thing that I never am able to actually get to run?
- 2067 is an interactive map for the 2018 election.
- 2198 is actually HTML? Weird.

Outliers
- 191 has a link to a different version of the comic but with a different method of getting to it.
- 256 has a different way of getting to the image.
- 351 has a link to the rick roll video.
- 426 has a link to a geohash page that doesn't seem to work aymore?
- 482 has a link to the store for buying the comic as a poster.
- 514 Has a link to Wikipedia.
- 609 has a link to TVTropes
- 980 links to a huge image that has to be read specially.
- 1017 links to a spreadsheet.
- 1031 links to an archived wiki.
- 1052 has a link to a video of Modern Major General.
- 1104 links to a youtube video that no longer exists.
- 1169 has a link to the google map for a spot in Northen Russia.
- 1190 links to an interesting timeline playing gif that you can pause.
- 1506 Has a button to do some sort of pseudo facebook reporting thing.
- 1551 Link to a nasa article about Pluto.
- 1572 Links to a survey
- 1723 Links to an article on meteorites.
- 2005 Links to a New Yorker article about Thomas the Tank Engine.
- 2050 Links to an older comic.
- 2116 Links to Twitter.
- 2131 Links to an xkcd blog post.
- 2190 Links to an xkcd blog post.
- 2194 Links to an xkcd blog post.
- 2206 Links to a font site.
- 2234 Links to a book.
- 2380 Links to a PDF about voting.
- 2500 Links to research about global warming.
- 2575 Links to a book.
- 2600 Links to a book.
- 2609 Links to a video about Lord of the Rings.
- 2613 Links to a website about Mercator projections.
- 2636 Links to a book.
- 2655 Links to a book.
- 2662 Links to a book.
- 2669 Links to a book.
- 2672 "" ""

Personal Favorites
- 1513 Makes fun of bad code
- 1688 Huge flowchart of map stuff. Good test for if a hugh resultion version was ever downloded.
- 2160 Makes fun of crazy fan theories about a shared universe...WHO CARES?!
- 2224 Is about software updates.
"""

# TODO - Find a better way to get the end point.


class XkcdScraper(ComicScraper):
    WAIT_TIME = 1
    COMIC_BASE_URL = 'https://xkcd.com/'
    IMAGE_URL = 'https://imgs.xkcd.com/comics/'
    IMAGE_STRIP_PREFIX = '//imgs.xkcd.com/comics/'
    COMIC_SKIP_SET = (404, 1350, 1416, 1525, 1608, 1663, 2067, 2198)
    OUTLIER_COMIC_SET = ("191", "351", "426", "482",
                         "514", "609", "851", "871",
                         "980", "1017", "1031", "1052", "1104", "1169", "1190", '1506', '1551', '1572', '1723', '2005', '2050', '2116', '2190', '2194', '2206', '2234', '2380', '2500', '2575', '2600', '2609', '2613', '2636', '2655', '2662', '2669', '2672', '2702')

    def __init__(self):
        self._logger = Logger('xkcd')

    def get_all_comics(self) -> None:
        comic_number = 1
        last_comic_number = self._most_recent_comic_number()
        self._create_xkcd_directory()
        while comic_number < last_comic_number:
            self._set_range(comic_number)
            self._create_image_range_directory()
            if comic_number not in self.COMIC_SKIP_SET and not self._check_if_file_exists(comic_number):
                image, image_name = self._getImageFile(str(comic_number))
                if image:
                    self._save_image(image, comic_number, image_name)
                    sleep(self.WAIT_TIME)
                else:
                    self._logger.log_error(
                        'Error with comic: {}'.format(str(comic_number)))
            comic_number += 1
            self._clear_range()
        print('Ended with comic # {}'.format(str(comic_number - 1)))

    def _getImageFile(self, comicNumber: str) -> Tuple[bytes, str]:
        try:
            data = requests.get(self.COMIC_BASE_URL + comicNumber)
            if BeautifulSoup(data.content, 'html.parser').find(id='comic').a:
                if comicNumber in self.OUTLIER_COMIC_SET:
                    image_tag = BeautifulSoup(
                        data.content, 'html.parser').find(id='comic').a.img
                else:
                    large_image_url = BeautifulSoup(
                        data.content, 'html.parser').find(id='comic').a.attrs['href']
                    if large_image_url.endswith('.png') or large_image_url.endswith('.jpeg') or large_image_url.endswith('.jpeg') or large_image_url.endswith('.gif'):
                        return self._get_large_image_from_image_url(large_image_url)
                    else:
                        return self._get_large_image_from_url(large_image_url)
            else:
                image_tag = BeautifulSoup(
                    data.content, 'html.parser').find(id='comic').img
            image_name = self._get_image_name_from_image_tag_src(
                image_tag.attrs['src'])
            image_response = requests.get(self.IMAGE_URL + image_name)
            if image_response.status_code == 200 and image_response.content:
                return (image_response.content, image_name)
            else:
                return (None, None)
        except:
            print('Error looking for comic {}'.format(comicNumber))
            return (None, 'error')

    def _get_large_image_from_image_url(self, image_url) -> Tuple[bytes, str]:
        """
        Gets the image from a url found in the first image tag that links to an actual image, not another page holding the image.
        So far the only comics that will fall into this are 256
        Page with the image tag for the smaller version -> ACTUAL image.
        """
        image_response = requests.get(image_url)
        return (image_response.content, image_url.replace('https://imgs.xkcd.com/comics/', ''))

    def _get_large_image_from_url(self, large_image_url: str) -> Tuple[bytes, str]:
        """
        Gets an image from a page that is linked to in the original image page.
        So far this is only for comic 191
        page with image tag of the smaller image -> page with the larger version of the image tag -> ACTUAL image file.
        """
        try:
            data = requests.get(large_image_url)
            image_tag = BeautifulSoup(data.content, 'html.parser').img
            image_response = requests.get(image_tag.attrs['src'])
            return (image_response.content, image_tag.attrs['src'].replace('https://imgs.xkcd.com/comics/', ''))
        except:
            print('Error getting the larger image.')
            return (None, 'error')

    def _get_image_name_from_image_tag_src(self, image_tag_src: str) -> str:
        return image_tag_src.replace(self.IMAGE_STRIP_PREFIX, '')

    def _create_xkcd_directory(self) -> None:
        if not os.path.exists(os.path.join('images', 'xkcd')):
            os.mkdir(os.path.join('images', 'xkcd'))

    def _create_image_range_directory(self) -> None:
        if not os.path.exists(os.path.join('images', 'xkcd', self.range)):
            print("Range {} does not exist. Creating it.".format(self.range))
            os.mkdir(os.path.join('images', 'xkcd', self.range))

    def _set_range(self, comic_number: int) -> None:
        self.range = "{}-{}".format(str((comic_number) // 100 * 100),
                                    str((((comic_number) // 100) + 1) * 100 - 1))

    def _clear_range(self) -> None:
        self.range = None

    def _check_if_file_exists(self, comic_number: int) -> bool:
        for file in os.listdir(os.path.join('images', 'xkcd', self.range)):
            if file.startswith("{}-".format(str(comic_number))):
                return True
        return False

    def _save_image(self, image: bytes, comic_number: int, filename: str) -> None:
        filepath = os.path.join(
            'images', 'xkcd', self.range, "{}-{}".format(comic_number, filename.replace('/', '-')))
        print("Saving comic {} with the name of {}".format(
            str(comic_number), filepath))
        open(filepath, 'wb').write(image)

    def _most_recent_comic_number(self) -> int:
        return 2703
