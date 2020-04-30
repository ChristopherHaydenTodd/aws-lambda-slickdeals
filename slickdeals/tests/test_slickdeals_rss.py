#!/usr/bin/env python3
"""
    Purpose:
        Test File for slickdeals_rss.py and SlickdealsRss
"""

# Python Library Imports
import os
import sys
import pytest
from unittest import mock

# Local Library Imports
BASE_PROJECT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/../"
sys.path.insert(0, BASE_PROJECT_PATH)
from slickdeals.slickdeals_rss import SlickdealsRss


###
# Mocks
###


# N/A


###
# Data Fixtures
###


# N/A


###
# Test Compliation/Syntax
###


def test_compile():
    """
    Purpose:
        Test that imports work, and get high level assurance of code
    Args:
        N/A
    """

    assert True


###
# Test Class Init
###


def test_class_init():
    """
    Purpose:
        Test that Initalizing SlickdealsRss works
    Args:
        N/A
    """

    slickdeals_rss_obj = SlickdealsRss()
