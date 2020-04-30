#!/usr/bin/env python3
"""
    Purpose:
        SlickdealsRss Class. Handles requesting data from Slickdeals RSS feed and
        parsing the results into consumable components
"""

# Python Library Imports
import feedparser
import logging
import requests


###
# Class Definition
###


class SlickdealsRss(object):
    """
        SlickdealsRss Class. Handles requesting data from Slickdeals RSS feed and
        parsing the results into consumable components
    """

    ###
    # Class Properties
    ###

    urls = {
        "frontpage": (
            "https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&"
            "searchin=first&rss=1"
        ),
        "popular": (
            "https://slickdeals.net/newsearch.php?mode=popdeals&searcharea=deals&"
            "searchin=first&rss=1"
        ),
    }

    ###
    # Class Lifecycle Methods
    ###

    def __init__(self):
        """
        Purpose:
            Initilize the SlickdealsRss Class.
        Args:
            N/A
        Returns:
            N/A
        """
        logging.debug("Initializing SlickdealsRss")

    ###
    # Get Data Methods
    ###

    @classmethod
    def get_deals(cls):
        """
        Purpose:
            Get deals from all Slickdeals RSS Feeds.
        Args:
            N/A
        Return:
            deals (List of Dicts): Deals that have been found in the available feeds
        """
        logging.info(f"Getting Deals from SlickDeals RSS Feeds")

        deals = []

        # Get deals from each feed
        for feed_name in cls.urls.keys():
            deals += cls.get_deals_from_feed(feed_name)

        # Remove Duplicates
        deals = list(set(deals))

        return deals

    ###
    # Request Data from Slickdeals UI Methods
    ###

    @classmethod
    def get_deals_from_feed(cls, feed):
        """
        Purpose:
            Get deals from a Slickdeals RSS Feed. Choose a feed name
            from the possible feeds
        Args:
            feed (String): Name of the feed to pull from
        Return:
            deals (List of Dicts): Deals that have been found in the feed
        """
        logging.info(f"Getting Deals from SlickDeals RSS Feed: {feed}")

        # Verify feed is known
        if feed not in cls.urls:
            raise Exception(f"{feed} not a known Slickdeals Feed")

        return [
            deal
            for deal
            in feedparser.parse(cls.urls.get(feed))["entries"]
        ]
