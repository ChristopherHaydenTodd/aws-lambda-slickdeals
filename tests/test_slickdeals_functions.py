#!/usr/bin/env python3
"""
    Purpose:
        Test Slickdeals Functions

    function call:
        python3 test_slickdeals_funcions.py
"""

# Python Library Imports
import json
import logging
import os
import sys
from argparse import ArgumentParser

# Local Library Imports
PROJECT_BASE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/../"
sys.path.insert(0, PROJECT_BASE_PATH)
from utils import loggers
from utils import slickdeals


###
# Main Functionality
###


def main():
    """
    Purpose:
        Main Execution for Running Example Requests
    Args:
        N/A
    Return:
        N/A
    """

    # lambda_entrypoint

    deals_with_filter =\
        slickdeals.get_slickdeals(raw_deal_filter="Tomb\n")
    deals_no_filter = slickdeals.get_slickdeals()

    import pdb; pdb.set_trace()


###
# Execute Function
###

if __name__ == "__main__":

    loggers.clear_log_handlers()
    logging = loggers.get_stdout_logging(
        log_level=logging.INFO, log_prefix="[test_slickdeals_funcions]: "
    )

    try:
        main()
    except Exception as err:
        logging.exception(
            "{0} failed due to error: {1}".format(os.path.basename(__file__), err)
        )
        raise
