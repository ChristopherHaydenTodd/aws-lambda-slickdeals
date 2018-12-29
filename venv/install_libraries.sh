#!/usr/bin/env bash
#
# Install Required Libraries
#

if [[ -z "$VIRTUAL_ENV" ]]
then
  echo "Python Virtual Environment is NOT Active. You need to be active to install libaries"
  exit 1
fi

echo "$(date +%c): Installing Required Packages"
pip3 install -r requirements.txt
