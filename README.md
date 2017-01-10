# cogito-resource

A CloudFormation [custom resource](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) lambda handler that enables you to write [cogito](https://github.com/localytics/libcogito) syntax in your CloudFormation templates.

## Dependencies

Ensure you have [`serverless`](https://serverless.com/) and [`pip`](https://pypi.python.org/pypi/pip) installed.

## Getting started

Download the latest `libcogito` from the Localytics public S3 endpoint:

    curl https://s3.amazonaws.com/public.localytics/artifacts/cogito/amazon/libcogito.so -o libcogito.so

Install the python dependencies into the `vendor` directory:

    pip install -t vendor -r requirements.txt

Run `serverless` to deploy:

    serverless deploy

Take that outputted arn for the lambda and use that to build a custom resource in CloudFormation like:

```json
{
  "Resources": {
    "CogitoResource": {
      "Type": "Custom::CogitoResource",
      "Version": "1.0",
      "Properties": {
        "ServiceToken": "arn:aws:lambda:us-east-1:000123456789:function:cogito-dev-cogito",
        "Policy": "ALLOW s3:GetObject ON *;"
      }
    },
    "CogitoPolicy": {
      "Type": "AWS::IAM::ManagedPolicy",
      "Properties": {
        "PolicyDocument": { "Fn::GetAtt": ["CogitoResource", "PolicyDocument"] }
      }
    }
  }
}
```

Deploy your CloudFormation stack and you will now have an IAM ManagedPolicy resource with the expanded IAM permission syntax below:

```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject"
  ],
  "Resource": "*"
}
```

For a more verbose example, see the [example](example) directory.
