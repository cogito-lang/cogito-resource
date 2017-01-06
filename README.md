# cogito-resource

A CloudFormation custom resource lambda handler that enables you to write [cogito](https://github.com/localytics/libcogito) syntax in your CloudFormation templates.

## Getting started

Download the latest `libcogito` from the Localytics public S3 endpoint:

    curl https://s3.amazonaws.com/public.localytics/artifacts/cogito/amazon/libcogito.so -o libcogito.so

Install the dependencies into the `vendor` directory:

    pip install -t vendor -r requirements.txt

Ensure you have [`serverless`](https://serverless.com/) installed:

    npm install -g serverless

Run `serverless` to deploy:

    serverless deploy
