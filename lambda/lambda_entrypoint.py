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
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

# Local Library Imports
from utils import loggers

# Configure Logging
loggers.clear_log_handlers()
logging = loggers.get_stdout_logging(
    log_level=logging.INFO, log_prefix="[slickdeals_deals]: "
)

# Globals
SLICKDEALS_URL = "https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1"
SKILL_BUILDER = SkillBuilder()

###
# Request Handlers
###


@SKILL_BUILDER.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """
    Purpose:
        Handler The Launching of the Alexa Skill 
    Args:
        handler_input (Dict): Input data from the Alexa Skill 
    Return:
        alexa_reponse (Dict): Reponse for Alexa Skill to handle
    """
    speech_text = "Welcome to the Slick Deals Alexa Skill"

    return (
        handler_input.response_builder.speak(speech_text)
        .set_card(SimpleCard("Slick Deals", speech_text))
        .set_should_end_session(False)
        .response
    )


@SKILL_BUILDER.request_handler(can_handle_func=is_intent_name("GetNewDealsIntent"))
def get_new_deals_intent_handler(handler_input):
    """
    Purpose:
        Handler for getting new deals
    Args:
        handler_input (Dict): Input data from the Alexa Skill
    Return:
        alexa_reponse (Dict): Reponse for Alexa Skill to handle
    """

    feed = get_slickdeals_feed(SLICKDEALS_URL)
    deals = get_top_slickdeals(feed)

    speech_text = "There are {0} deals. The first deal is {1}".format(
        len(deals), deals[0]
    )

    return (
        handler_input.response_builder.speak(speech_text)
        .set_card(SimpleCard("Slick Deals", speech_text))
        .set_should_end_session(True)
        .response
    )


@SKILL_BUILDER.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """
    Purpose:
        Handler for getting help for the skill 
    Args:
        handler_input (Dict): Input data from the Alexa Skill
    Return:
        alexa_reponse (Dict): Reponse for Alexa Skill to handle
    """

    speech_text = "There is no help yet"

    return (
        handler_input.response_builder.speak(speech_text)
        .set_card(SimpleCard("Slick Deals", speech_text))
        .set_should_end_session(False)
        .response
    )


@SKILL_BUILDER.request_handler(
    can_handle_func=lambda handler_input: is_intent_name("AMAZON.CancelIntent")(
        handler_input
    )
    or is_intent_name("AMAZON.StopIntent")(handler_input)
)
def cancel_and_stop_intent_handler(handler_input):
    """
    Purpose:
        Handler for cancelling or stopping the skill
    Args:
        handler_input (Dict): Input data from the Alexa Skill
    Return:
        alexa_reponse (Dict): Reponse for Alexa Skill to handle
    """

    speech_text = "Goodbye!"

    return (
        handler_input.response_builder.speak(speech_text)
        .set_card(SimpleCard("Hello World", speech_text))
        .response
    )


@SKILL_BUILDER.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """
    Purpose:
        Handler for cancelling or stopping the skill

        Note: AMAZON.FallbackIntent is only available in en-US locale.
        This handler will not be triggered except in that locale,
        so it is safe to deploy on any locale.
    Args:
        handler_input (Dict): Input data from the Alexa Skill
    Return:
        alexa_reponse (Dict): Reponse for Alexa Skill to handle
    """

    speech_text = "That request is not available, try something else"
    reprompt_text = "try something else"

    handler_input.response_builder.speak(speech_text).ask(reprompt_text)
    return handler_input.response_builder.response


@SKILL_BUILDER.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """
    Purpose:
        Handler for ending the session 
    Args:
        handler_input (Dict): Input data from the Alexa Skill
    Return:
        alexa_reponse (Dict): Reponse for Alexa Skill to handle
    """

    return handler_input.response_builder.response


@SKILL_BUILDER.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """
    Purpose:
        Handler for all exceptions
    Args:
        handler_input (Dict): Input data from the Alexa Skill causing
            causing the exception
        exception (Exception Object): Excemption raised
    Return:
        alexa_reponse (Dict): Reponse for Alexa Skill to handle
    """
    logger.error(exception, exc_info=True)

    speech_text = "Sorry, there was some problem. Please try again"
    handler_input.response_builder.speak(speech_text).ask(speech_text)

    return handler_input.response_builder.response

handler = SKILL_BUILDER.lambda_handler()
###
# Slickdeals Functions
###


def get_slickdeals(event, context):
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
