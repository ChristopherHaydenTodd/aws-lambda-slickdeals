#!/usr/bin/env python3
"""
    Purpose:
        Library for getting loggers of specific configurations in Python.
        This will utilize Pythons built-in logging library and will return
        an instance of logging that can be implemented in any code
        taht already implements the logging class.
"""

# Python Library Imports
import feedparser
import inspect
import logging
import re
import sys


# Globals
SLICKDEALS_URLS = [
    "https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1",
    "https://slickdeals.net/newsearch.php?mode=popdeals&searcharea=deals&searchin=first&rss=1",
]


###
# Slickdeals Functions
###


def get_slickdeals(deal_filters=None):
    """
    Purpose:
        Function to get slickdeals from the Slickdeals RSS Feed
    Args:
        raw_deal_filter (String): String for filtering deals
    Return:
        N/A
    """
    logging.info("Starting Function to pull top slickdeals")

    feeds = get_slickdeals_feed(SLICKDEALS_URLS)

    deals = []
    for feed in feeds:
        for deal in get_top_slickdeals(feed, deal_filters=deal_filters):
            deals.append(
                clean_deal_title(
                    shorten_deal_title(
                        deal
                    )
                )
            )

    deals = list(set(deals))
    deals.sort()

    logging.info("Function to pull top slickdeals Complete")

    return deals


def get_top_slickdeals(feed, deal_filters=None):
    """
    Purpose:
        Responsible for looping through the feed object and pulling the
        top 25 deals and filtering out any deals that do not match the
        keyword provided
    Args:
        feed (Feed Object): Feed object from feedparser of the RSS Feed
        deal_types (List of Strings): list of keyword filters
    Return:
        deals (List of Strings): Title of all deals pulled
    """
    logging.info("Geting Top SlickDeals")

    deals = []

    if deal_filters:
        for deal in feed["entries"]:
            deal_passes_filter = False

            for deal_filter in deal_filters:
                if deal_filter in deal["title"].lower():
                    deal_passes_filter = True
                    break

            if deal_passes_filter:
                deals.append(deal["title"])
    else:
        deals = [
            deal["title"]
            for deal
            in feed["entries"]
        ]

    return deals


def get_slickdeals_feed(feed_urls):
    """
    Purpose:
        Responsible for establising a feed object subscribed to the
        Slickdeals top deals feed
    Args:
        feed_url (String): URL of the top deals feed from slickdeals
    Return:
        feed (Feed Object): Feed object from feedparser of the RSS Feed
    """
    logging.info("Getting Slickdeals Feed")

    return [
        feedparser.parse(feed_url)
        for feed_url
        in feed_urls
    ]


###
# Slickdeals Personal Favorites
###


def get_chris_filters():
    """
    Purpose:
        Get filters that Chris likes to search
    Args:
        N/A
    Return:
        deal_filters (List of Strings): Deal Type Filter to filter deals
            in SlickDeals
    """

    return [
        "baby",
        "dog",
        "dunkin",
        "free",
        "gift card",
        "marriott",
        "nfl",
        "nintendo",
        "photo",
        "ps4",
        "psvr",
        "smart home",
        "steam",
        "xbox",
    ]


def get_brittany_filters():
    """
    Purpose:
        Get filters that Brittany likes to search
    Args:
        N/A
    Return:
        deal_filters (List of Strings): Deal Type Filter to filter deals
            in SlickDeals
    """

    return [
        "disney",
    ]


###
# Helper Functions
###


def parse_raw_deal_filters(raw_deal_filter):
    """
    Purpose:
        Parse raw_deal_filter into a format that is usuable for
        comparing against the slickdeals
    Args:
        raw_deal_filter (String): String of some filter object to
            filter out deals
    Return:
        deal_filters (List of Strings): Deal Type Filter to filter deals
            in SlickDeals
    """
    logging.info("Parsing Raw Deal Filters")

    # Lower Case
    deal_filters = raw_deal_filter.lower()

    # Stripping Non Alpha-Numeric Characters and Converting to List
    alphanumeric_pattern = r"\w+"
    deal_filters = re.findall(alphanumeric_pattern, deal_filters)

    return deal_filters


def shorten_deal_title(deal_title, words_to_keep=10):
    """
    Purpose:
        Shorten the deal title to a number of words
    Args:
        deal_title (String): Title to shorten
        words_to_keep (Int): Number of words to keep
    Return:
        short_deal_title (String): Shortened Deal Title
    """
    logging.info(f"Shortening Title {deal_title} to {words_to_keep} words")

    return " ".join(deal_title.split()[:words_to_keep])


def clean_deal_title(deal_title):
    """
    Purpose:
        Clean deal title for text to speech.
    Args:
        deal_title (String): Title to clean
    Return:
        clean_deal_title (String): Cleaned Deal Title
    """
    logging.info("Cleaning Deal Title")

    # Stripping Non Alpha-Numeric Characters and Converting to List
    alphanumeric_pattern = r"[^A-Za-z0-9\ \$\.]+"
    clean_deal_title = re.sub(alphanumeric_pattern, "", deal_title)

    return clean_deal_title
