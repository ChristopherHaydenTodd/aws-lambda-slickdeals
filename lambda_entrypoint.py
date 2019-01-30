#!/usr/bin/env python3
"""
    Purpose:
        Lambda Function for Pulling the top deals
        from slickdeals
    Version: 1.0.1
"""

# Python Library Imports
from __future__ import print_function
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
from utils import slickdeals

# Configure Logging
loggers.clear_log_handlers()
logging = loggers.get_stdout_logging(
    log_level=logging.INFO, log_prefix="[slickdeals_deals]: "
)

# Globals
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
    logging.info("In the LaunchRequest Handler")

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
        Handler for getting new deals. Will pull deals from the RSS Feed and return them
    Args:
        handler_input (Dict): Input data from the Alexa Skill
    Return:
        alexa_reponse (Dict): Reponse for Alexa Skill to handle
    """
    logging.info("In the GetNewDealsIntent Handler")

    deals = slickdeals.get_slickdeals()

    if deals:
        speech_text = f"Here are the deals: "
        for idx, deal in enumerate(deals[:10]):
            speech_text += f"Deal number {idx+1} is {deal}. "
    else:
        speech_text = f"There are no deals"

    return (
        handler_input.response_builder.speak(speech_text)
        .set_card(SimpleCard("Slick Deals", speech_text))
        .set_should_end_session(True)
        .response
    )


@SKILL_BUILDER.request_handler(can_handle_func=is_intent_name("GetSpecificDealsIntent"))
def get_specfic_deals_intent_handler(handler_input):
    """
    Purpose:
        Handler for getting new deals. Will pull deals from the RSS Feed based on
        a specific filter and loop through until one is found
    Args:
        handler_input (Dict): Input data from the Alexa Skill
    Return:
        alexa_reponse (Dict): Reponse for Alexa Skill to handle
    """
    logging.info("In the GetSpecificDealsIntent Handler")

    request_slots = get_slots_from_request(handler_input)
    raw_deal_filter = request_slots["deal_type"].value

    deals =\
        slickdeals.get_slickdeals(raw_deal_filter=raw_deal_filter)

    if deals:
        speech_text = f"Here are the deals for {raw_deal_filter}: "
        for idx, deal in enumerate(deals[:10]):
            speech_text += f"Deal number {idx+1} is {deal}. "
    else:
        speech_text = f"There are no deals that match {raw_deal_filter}"

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
    logging.info("In the AMAZON.HelpIntent Handler")

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
    logging.info("In the AMAZON.CancelIntent/StopIntent Handler")

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
    logging.info("In the AMAZON.FallbackIntent")

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
    logging.info("In the SessionEndedRequest Handler")

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
    logging.exception(
        f"Exception in lambda_entrypoint: {exception}", exc_info=True
    )

    speech_text = "Sorry, there was some problem. Please try again"
    handler_input.response_builder.speak(speech_text).ask(speech_text)

    return handler_input.response_builder.response


handler = SKILL_BUILDER.lambda_handler()


###
# Helper Functions
###


def get_slots_from_request(handler_input):
    """
    Purpose:
        Parse out the Slots from the handler inputs
    Args:
        handler_input (Dict): Input data from the Alexa Skill
    Return:
        request_slots (Dict): Dict with Slots passed from the
            Request in the Alexda Skill
    """

    return handler_input.request_envelope.request.intent.slots


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
