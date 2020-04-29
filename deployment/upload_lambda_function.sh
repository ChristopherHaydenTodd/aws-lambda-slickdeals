#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Deploy Lambda Function Code by deploying the Zip file using the
# AWS Cli (installed with python)
#
# Arguments:
# N/A
#
# Example:
# sh create_deployable_zip.sh
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

FORCE=false
PWD=$(pwd)
VERSION=$(cat ../VERSION)
BASE_ZIP_FILENAME="slickdeals-top-deals"

# Parse CLI Arguments
while [ "$#" -gt 0 ]
do
    key="$1"

    case $key in
        -f|--force)
        FORCE=true
        shift
        ;;
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

if [[ -z "$VIRTUAL_ENV" ]]; then
  log "ERROR" "Python Virtual Environment is NOT Active. You need to be active to install libaries"
  exit 1
elif [[ "$VIRTUAL_ENV" != *"slickdeals-venv"* ]]; then
  log "ERROR" "Incorrect Python Virtual Environment is set, need 'slickdeals-venv' not '$VIRTUAL_ENV'"
  exit 1
fi


###
# Execute Commands
###


log "INFO" "Pushing Zip"
aws lambda update-function-code --function-name=slickdeals-top-deals --zip-file=fileb://slickdeals-top-deals.zip
