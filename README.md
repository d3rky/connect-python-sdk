# Connect Python  SDK

![pyversions](https://img.shields.io/pypi/pyversions/connect-sdk.svg)  [![PyPi Status](https://img.shields.io/pypi/v/connect-sdk.svg)](https://pypi.org/project/connect-sdk/) [![codecov](https://codecov.io/gh/ingrammicro/connect-python-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/ingrammicro/connect-python-sdk) [![Build Status](https://travis-ci.org/ingrammicro/connect-python-sdk.svg?branch=master)](https://travis-ci.org/ingrammicro/connect-python-sdk) [![PyPI status](https://img.shields.io/pypi/status/connect-sdk.svg)](https://pypi.python.org/pypi/connect-sdk/)

Connect Python SDK allows an easy and fast integration with Connect fulfillment API. Thanks to it you can automate the fulfillment of orders generated by your products.

Please check the documentation available [here](https://connect-python-sdk.readthedocs.io), which contains information on how to install and use the library, and a complete API reference guide.

## Main Features

This library may be consumed in your project in order to automate the fulfillment of requests, this class once imported into your project will allow you to:

- Communicate with Connect using your API credentials.
- List all requests, and even filter them:
  - For a specific product.
  - For a specific status.
  - For a specific asset.
  - Etc.
- Process each request and obtain full details of the request.
- Modify the activation parameters of each request in order to:
  - Inquiry for changes
  - Store information into the fulfillment request
- Change the status of the requests from its initial pending state to either inquiring, failed or approved.
- Generate and upload usage files to report usage for active contracts and listings.
- Process usage file status changes.
- Work with Notes for requests.
- Generate logs.
- Collect debug logs in case of failure.

Your code may use any scheduler to execute, from a simple cron to a cloud scheduler like the ones available in Azure, Google, Amazon or other cloud platforms.

## Installation

```sh
$ pip install connect-sdk
```

## Requirements

* Python 2.7+ or Python 3.4+
* Requests (https://pypi.org/project/requests/)
* Marshmallow (https://pypi.org/project/marshmallow/)

## Contribute

If you want to contribute to the connect-python-sdk development feel free to open issues or fork the github repository and submit your pull request.

## Development

### Getting started

Assuming that you have python and virtualenv installed, and forked the connect-python-sdk repository, set up your environment and install the required dependencies like this:

```sh
$ git clone https://github.com/{your_github_account}/connect-python-sdk.git
$ cd connect-python-sdk
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements/test.txt
```

### Running tests

The connect-python-sdk uses [pytest](https://docs.pytest.org/en/latest/) for unit testing.

To run the entire tests suite execute:

```sh
$ pytest
```

## License

The connect-python-sdk is released under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).


