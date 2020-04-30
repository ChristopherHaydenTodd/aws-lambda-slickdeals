#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Create Lambda Function Zip for Deploying Function
#
# This will include the code, libraries (pulled from the venv), and all
# local utilities
#
# Arguments:
# -z [value], --zip [value], --zip=[value]
#    Specify the zipfile base name
# -v [value], --version [value], --version=[value]
#    Specify the version to build
# -f, --force
#    Force the build if previous version exists
#
# Example:
# sh create_deployable_zip.sh [-h] [--node NODE] [--performer PERFORMER_NAME]
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

BASE_ZIP_FILENAME="slickdeals-top-deals"
FORCE=false
CURRENT_DIR=$(pwd)
VERSION=$(cat ../VERSION)

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
        -h|--help)
        echo "Usage: sh create_deployable_zip.sh [-h] [--version value] [--zip value] [--force]"
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

echo "$CURRENT_DIR"

log "INFO" "Running Tests"
cd ../
sh test_python_package.sh &> /dev/null
TEST_STATUS=$?
if [ "$TEST_STATUS" == "0" ]; then
    log "ERROR" "Tests Passed: ${TEST_STATUS}"
else
    log "ERROR" "Tests Failed: ${TEST_STATUS}"
    if ! $FORCE; then
      log "ERROR" "--force not set, exiting"
      exit 1
    else
      log "INFO" "--force set, Building even with failed tests"
    fi
fi
cd $CURRENT_DIR

log "INFO" "Packaging Zip File: $ZIP_FILENAME"

log "INFO" "Checking File Not Exists or Force"
if test -f "$ZIP_FILENAME"; then
  log "INFO" "Found Previous Version of Zip File"
  if ! $FORCE; then
    log "ERROR" "--force not set, exiting"
    exit 1
  else
    log "INFO" "--force set, Overwriting Zip File"
    rm -rf $ZIP_FILENAME
  fi
fi

log "INFO" "Creating Zip and Adding Lambda Entrypoint to Zip File"
zip -r -q -j $ZIP_FILENAME ../lambda_entrypoint/lambda_entrypoint.py

log "INFO" "Adding Utilities/Local Libraries to Zip File"
zip -r -q $ZIP_FILENAME ../utils/*.py ../slickdeals/*.py

log "INFO" "Adding PIP Installed Packages to Zip File"
cd ../environment/slickdeals-venv/lib/python3.7/site-packages/
zip -r9 -q $ZIP_FILENAME .
cd $CURRENT_DIR
