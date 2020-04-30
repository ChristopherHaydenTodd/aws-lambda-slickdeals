#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Get information about the currently deployed lambda
#
# Arguments:
# -a [value], --aws [value], --aws=[value]
#    AWS Profile to us to connect to AWS
# -l [value], --lambda [value], --lambda=[value]
#    Name of the lambda function to upload/overwrite
#
# Example:
# sh get_lambda_function.sh --aws=personal
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


AWS_PROFILE="default"
LAMBDA_FUNCTION="slickdeals-top-deals"

# Parse CLI Arguments
while [ "$#" -gt 0 ]
do
    key="$1"

    case $key in
        -a|--aws)
        AWS_PROFILE="$2"
        shift
        shift
        ;;
        --aws=*)
        eval AWS_PROFILE="${1#*=}"
        shift
        ;;
        -l|--lambda)
        LAMBDA_FUNCTION="$2"
        shift
        shift
        ;;
        --lambda=*)
        eval LAMBDA_FUNCTION="${1#*=}"
        shift
        ;;
        -h|--help)
        echo "Usage: sh get_lambda_function.sh [-h] [--aws value] [--lambda value]"
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


log "INFO" "AWS Profile: $AWS_PROFILE"
