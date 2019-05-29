import json
import os
import sys
import hashlib

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "vendor"))
import requests

if os.getenv("COGITO_PATH") is None:
    os.environ["COGITO_PATH"] = os.path.join(os.getcwd(), "libcogito.so")
import cogito

def handle(event, context):
    response = {
        "Status": "SUCCESS",
        "StackId": event["StackId"],
        "RequestId": event["RequestId"],
        "LogicalResourceId": event["LogicalResourceId"]
    }

    try:
        converted = cogito.to_json(
            event["ResourceProperties"]["Policy"],
            event["ResourceProperties"].get("Substitutions", {})
        )

        response["PhysicalResourceId"] = hashlib.md5(converted.encode("utf-8")).hexdigest()
        response["Data"] = {}
        response["Data"]["PolicyDocument"] = json.dumps({
            "Version": "2012-10-17",
            "Statement": json.loads(converted)
        })
    except cogito.CogitoError as exception:
        response["Status"] = "FAILED"
        response["Resource"] = exception.message

    requests.put(event["ResponseURL"], json.dumps(response))
    return response
