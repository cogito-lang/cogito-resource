# cogito-resource

A CloudFormation custom resource lambda handler that enables you to write [cogito](https://github.com/localytics/libcogito) syntax in your CloudFormation templates.

## Getting started

Run `make` to generate `output.zip`, which will have zipped up both the handler, the vendored `cogito` wrapper, and the `libcogito` shared object file that was compiled for Amazon Linux. You can then upload that zip as a lambda.
