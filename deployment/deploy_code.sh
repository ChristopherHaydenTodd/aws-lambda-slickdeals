#!/usr/bin/env bash
#
# Deploy Lambda Function Code
#

echo "$(date +%c): Pushing Zip"
aws lambda update-function-code --function-name=slickdeals-top-deals --zip-file=fileb://slickdeals-top-deals.zip
