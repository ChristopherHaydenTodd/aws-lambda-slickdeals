#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Run as test of the lambda function locally
#
# Arguments:
# N/A
#
# Example:
# sh test_local_lambda_requests.sh
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


VENV_NAME="slickdeals-venv"
REQUEST_OPTIONS=$(ls ./example_request_files/)
REQUEST_NAME=""

# Parse CLI Arguments
while [ "$#" -gt 0 ]
do
    key="$1"

    case $key in
        -r|--request)
        REQUEST_NAME="$2"
        shift
        shift
        ;;
        --request=*)
        eval REQUEST_NAME="${1#*=}"
        shift
        ;;
        -h|--help)
        echo "Usage: sh test_local_lambda_requests.sh [-h] [--request value]"
        echo "Available Requests:"
        echo "$REQUEST_OPTIONS"
        exit 1
        ;;
        *)
        log "ERROR" "Unknown argument \"$1\", exiting"
        exit 1
        ;;
    esac
done


###
# Check Environment
###


# Check Request Exists, and that its a valid option
if [[ "$REQUEST_NAME" == "" ]]; then
  log "ERROR" "Request Name not set (--request); Exiting"
  log "INFO" "Available Requests:"
  echo "$REQUEST_OPTIONS"
  exit 1
elif [[ "$REQUEST_OPTIONS" != *"$REQUEST_NAME"* ]]; then
  log "ERROR" "Request $REQUEST_NAME not available, Exiting"
  log "INFO" "Available Requests:"
  echo "$REQUEST_OPTIONS"
  exit 1
fi

# if no .json in the name, add it
if [[ "$REQUEST_NAME" != *".json"* ]]; then
  REQUEST_NAME="$REQUEST_NAME.json"
fi

# Set up Python virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
  log "INFO" "Python Virtual Environment is NOT Active. You need to be active to install libaries"
  exit 1
elif [[ "$VIRTUAL_ENV" != *"slickdeals-venv"* ]]; then
  log "INFO" "Incorrect Python Virtual Environment is set, need 'slickdeals-venv' not '$VIRTUAL_ENV'"
  exit 1
fi


###
# Execute Commands
###

log "INFO" "here"
python-lambda-local \
    -f handler \
    -l ../environment/$VENV_NAME/lib/ \
    ../lambda_entrypoint/lambda_entrypoint.py \
    ./example_request_files/$REQUEST_NAME

