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
SLICKDEALS_URL =\
    "https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1"


###
# Slickdeals Functions
###


def get_slickdeals(raw_deal_filter=None):
    """
    Purpose:
        Function to get slickdeals from the Slickdeals RSS Feed
    Args:
        raw_deal_filter (String): String for filtering deals
    Return:
        N/A
    """
    logging.info("Starting Function to pull top slickdeals")

    if raw_deal_filter:
        deal_filters = parse_raw_deal_filters(raw_deal_filter)
    else:
        deal_filters = None

    feed = get_slickdeals_feed(SLICKDEALS_URL)
    deals = get_top_slickdeals(feed, deal_filters=deal_filters)

    logging.info("Function to pull top slickdeals Complete")

    return deals


def get_slickdeals_feed(feed_url):
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

    return feedparser.parse(feed_url)


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
                deals.append(shorten_deal_title(deal["title"]))
    else:
        deals = [shorten_deal_title(deal["title"]) for deal in feed["entries"]]

    return deals


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
