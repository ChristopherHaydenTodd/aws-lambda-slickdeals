#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Clean Previously Built Python Package Package
#
# Arguments:
# N/A
#
# Example:
# sh clean_python_package.sh
# -----------------------------------------------------------------------------


###
# Helper Functions and Setup
###

set -e

function log {
  echo "$(date +%c) $1: $2"
}


###
# Execute Commands
###


log "INFO" "Cleaning Built Package (Removing Previous Build Artifacts)"
rm -rf \
  ./.coverage \
  ./.eggs/ \
  ./*.egg-info/ \
  ./build/ \
  ./dist/ \
  ./htmlcov/ \
  */.pytest_cache/ \
  */__pycache__ \
