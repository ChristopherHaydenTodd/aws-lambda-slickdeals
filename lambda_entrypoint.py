#!/usr/bin/env python3
"""
    Purpose:
        Lambda Function for Pulling the top deals
        from slickdeals
    Version: 1.0.0
"""

# Python Library Imports
from __future__ import print_function
import feedparser
import json
import logging
import os
import sys

# Local Library Imports
from utils import loggers

# Configure Logging
loggers.clear_log_handlers()
logging = loggers.get_stdout_logging(
    log_level=logging.INFO, log_prefix="[slickdeals_deals]: "
)

# Globals
SLICKDEALS_URL = "https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1"


###
# Main Entrypoint
###


def lambda_handler(event, context):
    """
    Purpose:
        Handler function for a Lambda function. Will take in an
        event object that triggers the function call and the context
        related to the event.
    Args:
        event (Dict): Dict with event details from the triggering event
            for the function.
        context (Dict): Metadata and context for the function call triggering
            the lambda function
    Return:
        N/A
    """
    logging.info("Starting Lambda to pull top slickdeals")

    feed = get_slickdeals_feed(SLICKDEALS_URL)
    deals = get_top_slickdeals(feed)

    logging.info("Lambda to pull top slickdeals Complete")

    return deals


###
# Slickdeals Functions
###


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

    return feedparser.parse(feed_url)


def get_top_slickdeals(feed, keyword=None):
    """
    Purpose:
        Responsible for looping through the feed object and pulling the
        top 25 deals and filtering out any deals that do not match the
        keyword provided
    Args:
        feed (Feed Object): Feed object from feedparser of the RSS Feed
        keyword (String): keyword to filter deals on (if applicable)
    Return:
        deals (List of Strings): Title of all deals pulled
    """

    if keyword:
        return [
            deal["title"]
            for deal in feed["entries"]
            if keyword.lower() in deal["title"].lower()
        ]
    else:
        return [deal["title"] for deal in feed["entries"]]


if __name__ == "__main__":

    try:
        example_event = {}
        example_context = []
        for deal in lambda_handler(example_event, example_context):
            logging.info(f"Deal Found: {deal}")
    except Exception as err:
        logging.exception(
            "{0} failed due to error: {1}".format(os.path.basename(__file__), err)
        )
        raise
