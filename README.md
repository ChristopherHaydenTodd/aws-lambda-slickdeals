# AWS Lambda Function for Returning Top Slickdeals

The aws-lambda-slickdeals repository is holds the code for a Lambda deployed function to AWS that is used by the "slickdeals-top-deals" Alexa app. The code is responsible for scraping slickdeals for deals as per the user's request.

## Table of Contents

- [Dependencies](#dependencies)
- [How Tos](#how-tos)
- [Notes](#notes)
- [TODO](#todo)

## Dependencies

### Python Packages

* ...

## How Tos

### Get Started Developing

1. Create a Virtual Environment with Python

```
./$ cd environment
./environment$ sh create_and_configure_venv.sh
>> Output
```

2. Activate the Virtual Environment

```
./environment$ source slickdeals-venv/bin/activate
>> Output
(slickdeals-venv) ./environment$ ...
```

3. Install all Required Packages


```
(slickdeals-venv) ./environment$ sh install_libraries.sh
>> Output
```

### Deploy a Release

1. Activate the Virtual Environment

```
./$ cd deployment
./deployment$ source ../environment/slickdeals-venv/bin/activate
>> Output
(slickdeals-venv) ./deployment$ ...
```

2. Package the Lambda Function (.zip)

```
(slickdeals-venv) ./deployment$ sh create_deployable_zip.sh
```

3. Deploy the Lambda Function

```
(slickdeals-venv) ./deployment$ sh upload_lambda_function.sh
```

### Test Locally

* ...

### Test in AWS

* ...

## Notes

* ...

## TODO

* ...
