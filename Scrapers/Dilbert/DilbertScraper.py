from typing import Tuple
import requests
import os
from datetime import datetime, timedelta
from time import sleep
# from html.parser import HTMLParser
from bs4 import BeautifulSoup

from ..ComicScraper import ComicScraper

# TODO - I suspect there is a memory leak in here somewhere.
# For some reason some of the comics error over and over again and then just start magically working. It seems random when it first happens but they error consistently...and then just work again.


class DilbertScraper(ComicScraper):
    WAIT_TIME = 1
    COMIC_BASE_URL = "https://dilbert.com/strip/"

    # TODO - Add error handling
    def get_all_comics(self):
        date = datetime(1989, 4, 16)
        destinationDate = datetime.now()
        while date < destinationDate:
            year = date.strftime("%Y")
            month = date.strftime("%m")
            day = date.strftime("%d")
            dateString = date.strftime("%Y-%m-%d")
            self._create_dilbert_image_directory()
            self._create_year_directory(year)
            self._create_month_directory(year, month)
            if not self._check_if_download_exists(year, month, day):
                print("searching for " + dateString)
                image, filetype = self._get_image_file(dateString)
                if image and filetype:
                    # TODO - This needs to have a more elegant way of handling the errors. Maybe add an else clause to log the errored ones since the filetype is missing a lot for some reason.
                    self._save_image(image, dateString, year, month, filetype)
                sleep(self.WAIT_TIME)
            date = date + timedelta(days=1)

    def _get_image_file(self, dateString: str) -> Tuple[bytes, str]:
        """
        TODO - Return None when image doesn't exist. Possibly add to a log when the file doesn't exist so that it can be investigated.
        """
        try:
            data = requests.get(self.COMIC_BASE_URL + dateString)
            image_tag = BeautifulSoup(data.content, 'html.parser').find(
                class_='img-responsive img-comic')
            image_url = image_tag.attrs['src']
            # print(image_tag.attrs['src'])
            image_response = requests.get(image_url)
            if image_response.status_code == 200 and image_response.content:
                return (image_response.content, self._get_content_type_from_headers(image_response.headers))
            else:
                return (None, None)
        except:
            print("Error looking for comic {}".format(dateString))
            return (None, None)

    def _get_content_type_from_headers(self, headers) -> str:
        if headers and headers['Content-Type']:
            content_type_header_value: str = headers['Content-Type']
            return content_type_header_value.replace('image/', '')
        else:
            return None

    def _create_dilbert_image_directory(self):
        if not os.path.exists('images'):
            self._create_image_directory()
        if not os.path.exists(os.path.join("images", "dilbert")):
            os.mkdir(os.path.join("images", "dilbert"))

    def _create_image_directory(self):
        if not os.path.exists('images'):
            os.mkdir('images')

    def _create_year_directory(self, year):
        if not os.path.exists(os.path.join('images', "dilbert", year)):
            os.mkdir(os.path.join('images', 'dilbert', year))

    def _create_month_directory(self, year, month):
        monthDirectoryPath = os.path.join('images', 'dilbert', year, month)
        if not os.path.exists(monthDirectoryPath):
            os.mkdir(monthDirectoryPath)

    # TODO - Add error handling.
    def _save_image(self, image, filename, year, month, filetype):
        filepath = "{}.{}".format(os.path.join(
            'images', 'dilbert', year, month, filename), filetype)
        print("Saving file {}".format(filepath))
        open(filepath, 'wb').write(image)

    def _check_if_download_exists(self, year, month, day):
        for file in os.listdir(os.path.join('images', 'dilbert', year, month)):
            if file.startswith("{}-{}-{}.".format(year, month, day)):
                return True
        return False
