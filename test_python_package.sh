#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Test Python Package using setuptools, pytest, pytest-cov
#
# Arguments:
# -c, --cov
#    Open/Run code coverage report
#
# Example:
# sh test_python_package.sh [-h] [-c]
# -----------------------------------------------------------------------------


###
# Helper Functions and Setup
###


function log {
  echo "$(date +%c) $1: $2"
}


###
# Arguments
###


SETUP_FILE="./setup.py"
OPEN_CODE_COVERAGE=false

# Parse CLI Arguments
while [ "$#" -gt 0 ]
do
    key="$1"

    case $key in
        -c|--cov)
        OPEN_CODE_COVERAGE=true
        shift
        ;;
        -h|--help)
        echo "Usage: sh test_python_package.sh [-h] [-c]"
        exit 1
        ;;
        *)
        shift
        ;;
        *)
        log "ERROR" "Unknown argument \"$1\", exiting"
        exit 1
        ;;
    esac
done


###
# Execute Commands
###


log "INFO" "Running Unit Tests (Setup File = ${SETUP_FILE})"
python3 ${SETUP_FILE} test

# Getting status of tests
TEST_STATUS=$?
if [ "$TEST_STATUS" == "0" ]; then
    log "INFO" "Tests Passed: ${TEST_STATUS}"
else
    log "ERROR" "Tests Failed: ${TEST_STATUS}"
fi

# Open Code Coverage only works on certain OS
if [ "$(uname -s)" == "Darwin" ] && $OPEN_CODE_COVERAGE; then
    log "INFO" "Opening the Test Coverage Report"
    open htmlcov/index.html
fi

