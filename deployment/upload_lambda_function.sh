#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Deploy Lambda Function Code by deploying the Zip file using the
# AWS Cli (installed with python)
#
# Arguments:
# -z [value], --zip [value], --zip=[value]
#    Specify the zipfile base name
# -v [value], --version [value], --version=[value]
#    Specify the version to build
#
# Example:
# sh upload_lambda_function.sh
# -----------------------------------------------------------------------------


###
# Helper Functions and Setup
###


set -e

function log {
  echo "$(date +%c) $1: $2"
}


###
# Arguments
###


AWS_PROFILE="default"
BASE_ZIP_FILENAME="slickdeals-top-deals"
LAMBDA_FUNCTION="slickdeals-top-deals"
PWD=$(pwd)
VERSION=$(cat ../VERSION)

# Parse CLI Arguments
while [ "$#" -gt 0 ]
do
    key="$1"

    case $key in
        -z|--zip)
        BASE_ZIP_FILENAME="$2"
        shift
        shift
        ;;
        --zip=*)
        eval BASE_ZIP_FILENAME="${1#*=}"
        shift
        ;;
        -v|--version)
        VERSION="$2"
        shift
        shift
        ;;
        --version=*)
        eval VERSION="${1#*=}"
        shift
        ;;
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
        echo "Usage: sh upload_lambda_function.sh [-h] [--version value] [--zip value] [--aws value] [--lambda value]"
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
# Check Environment
###


ZIP_FILENAME="$PWD/releases/$BASE_ZIP_FILENAME-$VERSION.zip"


###
# Execute Commands
###


log "INFO" "AWS Profile: $AWS_PROFILE"
log "INFO" "Pushing Zip ($ZIP_FILENAME) to Lambda Function ($LAMBDA_FUNCTION)"
aws lambda update-function-code \
  --profile=$AWS_PROFILE \
  --function-name=$LAMBDA_FUNCTION \
  --zip-file=fileb://$ZIP_FILENAME