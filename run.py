from Scrapers import BusinessCatScraper, CalvinAndHobbesScraper, DilbertScraper, GarfieldScraper, OverTheHedgeScraper, XkcdScraper
import sys


def get_business_cat():
    scraper = BusinessCatScraper()
    scraper.get_all_comics()


def get_calvin_and_hobbes():
    scraper = CalvinAndHobbesScraper()
    scraper.get_all_comics()


def get_dilbert():
    scraper = DilbertScraper()
    scraper.get_all_comics()


def get_garfield():
    scraper = GarfieldScraper()
    scraper.get_all_comics()


def get_over_the_hedge():
    scraper = OverTheHedgeScraper()
    scraper.get_all_comics()


def get_xkcd():
    scraper = XkcdScraper()
    scraper.get_all_comics()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You need to give an argument!\n Available options:\ndilbert\nxkcd")
    if "businesscat" in sys.argv or "business-cat" in sys.argv:
        get_business_cat()
    if "calvin" in sys.argv or "calvin-and-hobbes" in sys.argv or "calvinandhobbes" in sys.argv:
        get_calvin_and_hobbes()
    if "dilbert" in sys.argv or "Dilbert" in sys.argv:
        get_dilbert()
    if "garfield" in sys.argv:
        get_garfield()
    if "overthehedge" in sys.argv or "over-the-hedge" in sys.argv:
        get_over_the_hedge()
    if "xkcd" in sys.argv:
        get_xkcd()
