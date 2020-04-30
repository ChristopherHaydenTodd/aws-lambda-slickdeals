"""
    Purpose:
        Utilities for working with Slickdeals.
"""

# Python Library Imports
import logging
import re


###
# Filter Deals
###


def filter_deals(deals, deal_filters=None):
    """
    Purpose:
        Filter deals passed in
    Args:
        deals (List of Dicts): Deals to filter
        deal_filters (List of Strings): list of keyword filters
    Return:
        filtered_deals (List of Strings): Filtered Deals
    """
    logging.info("Filter Deals")

    filtered_deals = []

    if deal_filters:
        for deal in deals:
            deal_passes_filter = False

            for deal_filter in deal_filters:
                if deal_filter in deal["title"].lower():
                    deal_passes_filter = True
                    break

            if deal_passes_filter:
                filtered_deals.append(deal)
    else:
        filtered_deals = deals

    return filtered_deals


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


###
# Clean Deal/Title Functions
###


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
    alphanumeric_pattern = r"[^A-Za-z0-9\ \$\.\-]+"
    clean_deal_title = re.sub(alphanumeric_pattern, "", deal_title)

    return clean_deal_title


def format_deals_for_speach(deals, deal_filter=None):
    """
    Purpose:
        Convert deals list into string to text to speech.
    Args:
        deals (List of Strings): String (titles) of deals
    Return:
        speech_text (String): String representation for deals to pass
            back to Alexa
    """

    speech_text = None

    if not deal_filter:
        deal_filter = ""

    if deals:
        speech_text = f"Here are the {deal_filter} deals: "
        for idx, deal in enumerate(deals[:10]):
            formatted_deal_title = clean_deal_title(
                shorten_deal_title(
                    deal["title"]
                )
            )
            speech_text += f"{formatted_deal_title}. "
    else:
        speech_text = f"There are no {deal_filter} deals."

    return speech_text


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
