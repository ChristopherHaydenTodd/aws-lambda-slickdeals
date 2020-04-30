#!/usr/bin/env python3
"""
    Purpose:
        Test File for slickdeals_utils.py
"""

# Python Library Imports
import os
import sys
import pytest
from unittest import mock

# Local Library Imports
BASE_PROJECT_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/../"
sys.path.insert(0, BASE_PROJECT_PATH)
from slickdeals import slickdeals_utils


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
