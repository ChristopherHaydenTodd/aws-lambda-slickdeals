#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Install Required Libraries in the correct location (ensures)
# Virtual Environment is correct. This is required as the libraries
# need to be properly packaged with the code for deployment.
#
# Arguments:
# N/A
#
# Example:
# sh install_libraries.sh
# -----------------------------------------------------------------------------


###
# Helper Functions and Setup
###


set -e

function log {
  echo "$(date +%c) $1: $2"
}


###
# Check Environment
###


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


log "INFO" "Installing Required Packages"
pip3 install -r requirements.txt
