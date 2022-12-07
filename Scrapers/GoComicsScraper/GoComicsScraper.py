import requests
import os
from bs4 import BeautifulSoup
from datetime import date, timedelta
from time import sleep
from typing import Tuple

from Logger import Logger

"""
TODO - Can the date to string function be called once and turned into an object property?
    This would need to be reset as it changes constantly. 
    Would this cause memory issues? This could be what is causing issues in the other scrapers.
TODO - Allow a list of skippable dates to be passed into the get_all... function.
"""


class GoComicsScraper:
    WAIT_TIME = 1
    WEBSITE_BASE_URL = "https://www.gocomics.com/"

    def __init__(self, comic_name: str, comic_path: str):
        self._comic_path = comic_path
        self._logger = Logger(comic_path, comic_name)
        self._create_image_directory()
        self._create_comic_directory()

    def get_all_comics_in_range(self, start_date: date, end_date: date, *, interval: int = 1, skip_dates: Tuple[date] = [], skip_days_of_the_week: list[int] = []):
        """
        For skip_days_of_the_week, the numbers start with 0 being Monday and 6 being Sunday.
        """
        if start_date > end_date:
            assert (
                "Start date must be before end date or at the latest, the same day!")
        date = start_date
        while date <= end_date:
            if date not in skip_dates and date.weekday() not in skip_days_of_the_week:
                self._get_comic_by_date(date)

            date = date + timedelta(days=interval)

    def _get_comic_by_date(self, date: date) -> None:
        year = date.strftime("%Y")
        month = date.strftime("%m")
        day = date.strftime("%d")
        datestring = "{}/{}/{}".format(year, month, day)
        self._create_year_directory(year)
        self._create_month_directory(year, month)
        if not self._check_if_download_exists(date):
            print('searching for ' + datestring)
            image, filetype = self._get_comic_image(date)
            if image and filetype:
                self._save_image(image, filetype, year, month, day)
            sleep(self.WAIT_TIME)

    def _get_comic_image(self, date: date) -> Tuple[bytes, str]:
        try:
            url = "{}{}/{}/{}/{}".format(self.WEBSITE_BASE_URL, self._comic_path,
                                         date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"))
            data = requests.get(url)
            image_tag = BeautifulSoup(data.content, 'html.parser').find(
                class_='item-comic-image').img
            image_url = image_tag.attrs['src']
            image_response = requests.get(image_url)
            if image_response.status_code == 200 and image_response.content:
                return (image_response.content, self._get_image_type_from_headers(image_response.headers))
            return (None, None)
        except Exception as e:
            print(e)
            self._logger.log_error(
                "date: {} - {}".format(date.strftime("%Y-%m-%d"), e))
            return (None, None)

    def _get_image_type_from_headers(self, headers) -> str:
        if headers and headers['Content-Type']:
            content_type_header_value: str = headers['Content-Type']
            return content_type_header_value.replace('image/', '')
        else:
            return None

    # TODO - Can the image directory creation be simplified to just when the month is needed?

    def _create_image_directory(self) -> None:
        if not os.path.exists('images'):
            os.mkdir('images')

    def _create_comic_directory(self) -> None:
        if not os.path.exists(os.path.join('images', self._comic_path)):
            os.mkdir(os.path.join('images', self._comic_path))

    def _create_year_directory(self, year: str) -> None:
        if not os.path.exists(os.path.join('images', self._comic_path, year)):
            os.mkdir(os.path.join('images', self._comic_path, year))

    def _create_month_directory(self, year: str, month: str) -> None:
        if not os.path.exists(os.path.join('images', self._comic_path, year, month)):
            os.mkdir(os.path.join('images', self._comic_path, year, month))

    def _save_image(self, image: bytes, filetype: str, year, month, day) -> bool:
        try:
            filename = "{}-{}-{}.{}".format(year, month, day, filetype)
            self._create_month_directory(year, month)
            filepath = "{}".format(os.path.join(
                'images', self._comic_path, year, month, filename))
            print("Saving file {}".format(filepath))
            open(filepath, 'wb').write(image)
            return True
        except Exception as e:
            print(e)
            self._logger.log_error(e)
            return False

    def _check_if_download_exists(self, date: date) -> bool:
        filename = date.strftime("%Y-%m-%d")
        for file in os.listdir(os.path.join('images', self._comic_path, date.strftime("%Y"), date.strftime("%m"))):
            if file.startswith("{}.".format(filename)):
                return True
        return False
