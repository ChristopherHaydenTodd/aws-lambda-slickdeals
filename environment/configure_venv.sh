#!/usr/bin/env bash
#
# Install VENV
#

if [[ "$VIRTUAL_ENV" != "" ]]
then
  echo "Python Virtual Environment already exists; Exiting"
  exit 1
fi

echo "$(date +%c): Creating VENV"
python3.7 -m virtualenv .
