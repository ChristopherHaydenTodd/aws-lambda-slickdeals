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
# -a [value], --aws [value], --aws=[value]
#    AWS Profile to us to connect to AWS
# -l [value], --lambda [value], --lambda=[value]
#    Name of the lambda function to upload/overwrite
#
# Example:
# sh upload_lambda_function.sh --aws=personal
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
BASE_ZIP_FILENAME="slickdeals-top-deals"
BASE_CONFIG_FILENAME="config"
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
        -c|--config)
        BASE_CONFIG_FILENAME="$2"
        shift
        shift
        ;;
        --config=*)
        eval BASE_CONFIG_FILENAME="${1#*=}"
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


ZIP_FILENAME="$CURRENT_DIR/releases/$BASE_ZIP_FILENAME-$VERSION.zip"
log "INFO" "Checking Zip File Exists: $ZIP_FILENAME"
if ! test -f "$ZIP_FILENAME"; then
  log "ERROR" "Did Not Find Zip File; Exiting"
  exit 1
fi


###
# Execute Commands
###


log "INFO" "AWS Profile: $AWS_PROFILE"
log "INFO" "Pushing Zip ($ZIP_FILENAME) to Lambda Function ($LAMBDA_FUNCTION)"
aws lambda update-function-code \
  --profile=$AWS_PROFILE \
  --function-name=$LAMBDA_FUNCTION \
  --zip-file=fileb://$ZIP_FILENAME
