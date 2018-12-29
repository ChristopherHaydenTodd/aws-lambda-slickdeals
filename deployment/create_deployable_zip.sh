#!/usr/bin/env bash
#
# Create Lambda Function Zip for Deploying Function
#

if [[ -z "$VIRTUAL_ENV" ]]
then
  echo "Python Virtual Environment is NOT Active. You need to be active to push"
  exit 1
fi

echo "$(date +%c): Moving to Base Directory Previous Build"
cd ../

echo "$(date +%c): Removing Previous Build"
rm -rf deployment/slickdeals-top-deals.zip

echo "$(date +%c): Creating Zip and Adding Files"
zip -r deployment/slickdeals-top-deals.zip lambda_entrypoint.py utils/*.py

echo "$(date +%c): Moving to venv Package Directory"
cd venv/lib/python3.7/site-packages/

echo "$(date +%c): Adding Packages to Zip File)"
zip -r9 ../../../../deployment/slickdeals-top-deals.zip .
