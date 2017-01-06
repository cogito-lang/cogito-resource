# cogito-resource

A CloudFormation custom resource lambda handler that enables you to write [cogito](https://github.com/localytics/libcogito) syntax in your CloudFormation templates.

## Dependencies

Ensure you have [`serverless`](https://serverless.com/) and [`pip`](https://pypi.python.org/pypi/pip) installed.

## Getting started

Download the latest `libcogito` from the Localytics public S3 endpoint:

    curl https://s3.amazonaws.com/public.localytics/artifacts/cogito/amazon/libcogito.so -o libcogito.so

Install the python dependencies into the `vendor` directory:

    pip install -t vendor -r requirements.txt

Run `serverless` to deploy:

    serverless deploy
