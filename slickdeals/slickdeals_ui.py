"""
    Purpose:
        SlickdealsUi Class. Handles requesting data from Slickdeals website and
        parsing the results into consumable components
"""

# Python Library Imports
import inspect
import logging
import requests
from bs4 import BeautifulSoup


###
# Class Definition
###


class SlickdealsUi(object):
    """
        SlickdealsUi Class. Handles requesting data from Slickdeals website and
        parsing the results into consumable components
    """

    ###
    # Class Properties
    ###

    # Request Data
    expected_headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, sdch, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https: //www.indeed.com/",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    }
    urls = {
        "hot_deals": (
            "https://slickdeals.net/forums/filtered/?f=9&daysprune=7&order="
            "desc&pp={num_deals}&sort=threadstarted&vote=4"
        ),
    }

    # Slickdeals Business Logic
    blacklist_posts = [
        "RULES, FAQ, TIPS," # Ignore sticky post
    ]

    ###
    # Class Lifecycle Methods
    ###

    def __init__(self):
        """
        Purpose:
            Initilize the SlickdealsUi Class.
        Args:
            N/A
        Returns:
            N/A
        """
        logging.debug("Initializing SlickdealsUi")

    ###
    # Get Data Methods
    ###

    @classmethod
    def get_hot_deals(cls, num_deals=20):
        """
        Purpose:
            Get Hot Deals from Slickdeals UI; parse and return.
        Args:
            N/A
        Return:
            hot_deals (List of Dicts): Hot Deals that have been found
        """
        logging.info("Getting Hot Deals from SlickDeals")

        raw_hot_deals_html =\
            cls.request_hot_deals_from_slickdeals_ui(num_deals=num_deals)
        hot_deals = cls.parse_hot_deals_html(raw_hot_deals_html)

        return hot_deals

    ###
    # Request Data from Slickdeals UI Methods
    ###

    @classmethod
    def request_hot_deals_from_slickdeals_ui(cls, num_deals=20):
        """
        Purpose:
            Get Hot Deals from Slickdeals UI.
        Args:
            N/A
        Return:
            hot_deals (List of Dicts): Hot Deals that have been found
        """
        logging.info("Requesting Hot Deals from SlickDeals UI")

        logging.info(f"Fetching HTML from Slickdeals: {cls.urls['hot_deals']}")
        hot_deals_response = requests.get(
            cls.urls["hot_deals"].format(num_deals=num_deals),
            headers=cls.expected_headers
        )

        if hot_deals_response.status_code == 200:
            raw_hot_deals_html = hot_deals_response.text
        else:
            logging.error(
                "Got Failure Response from Slickdeals: "
                f"{hot_deals_response.status_code}"
            )
            raw_hot_deals_html = None

        return raw_hot_deals_html

    ###
    # HTML Parsing Methods
    ###

    @classmethod
    def parse_hot_deals_html(cls, raw_hot_deals_html):
        """
        Purpose:
            parse the HTML returned from Slickdeals with Beautiful Soup.
        Args:
            raw_hot_deals_html (String): HTML returned by Slickdeals UI
        Return:
            hot_deals (List of Dicts): Hot Deals that have been found
        """

        hot_deals = []

        # Parse Main DOM
        hot_deals_beautiful_soup = BeautifulSoup(raw_hot_deals_html, "html.parser")

        # Find the <tr> tags for each deal
        post_table_rows = hot_deals_beautiful_soup.findAll(
            "tr",
            id=lambda x: x and x.startswith("sdpostrow_")
        )

        # Find the HREF which has the deal title
        for post_table_row in post_table_rows:
            thread_title_hrefs = post_table_row.findAll(
                "a",
                id=lambda x: x and x.startswith("thread_title_")
            )

            # If more than one found, its unexpected. Skip
            if not thread_title_hrefs or len(thread_title_hrefs) > 1:
                continue

            # Ignore blacklist posts to slickdeals
            post_blacklisted = False
            for blacklist_post in cls.blacklist_posts:
                if blacklist_post in thread_title_hrefs[0].text:
                    post_blacklisted = True
                    break
            if post_blacklisted:
                continue

            # Append the link title to deals
            hot_deals.append({
                "title": thread_title_hrefs[0].text
            })

        # TODO, do we want to parse more data from the data?

        return hot_deals


if __name__ == "__main__":

    SlickdealsUi.get_hot_deals()
