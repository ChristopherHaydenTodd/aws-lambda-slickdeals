#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Publish Lambda Function Code, will create a new ARN and checkpoint
# the lambda function
#
# Arguments:
# -v [value], --version [value], --version=[value]
#    Specify the version to build
# -a [value], --aws [value], --aws=[value]
#    AWS Profile to us to connect to AWS
# -l [value], --lambda [value], --lambda=[value]
#    Name of the lambda function to upload/overwrite
#
# Example:
# sh publish_lambda_function.sh --aws=personal --version=1.1.0
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
LAMBDA_FUNCTION="slickdeals-top-deals"
VERSION=$(cat ../VERSION)

# Parse CLI Arguments
while [ "$#" -gt 0 ]
do
    key="$1"

    case $key in
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
        echo "Usage: sh publish_lambda_function.sh [-h] [--version value] [--aws value] [--lambda value]"
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
# Execute Commands
###

if [[ "$VERSION" != *"$(cat releases/releases.json)"* ]]; then
  log "ERROR" "$VERSION already published, not publishing"
  exit 1
fi

log "INFO" "AWS Profile: $AWS_PROFILE"

log "INFO" "Publishing Lambda Function Version $VERSION"
PUBLISHED_ARN=$(aws lambda publish-version \
  --profile=$AWS_PROFILE \
  --function-name=$LAMBDA_FUNCTION \
  | jq -r '.FunctionArn'
)
log "INFO" "Published Version $VERSION as $PUBLISHED_ARN"

log "INFO" "Storing ARN for Version $VERSION"
echo {"\"$VERSION\"": "\"$PUBLISHED_ARN\""} > current_release.json && \
  jq '.[] += input' releases/releases.json current_release.json > updated_releases.json && \
  rm current_release.json && \
  mv updated_releases.json releases/releases.json
