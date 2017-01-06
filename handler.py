import json
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, 'vendor'))
import requests

if os.getenv('COGITO_PATH') is None:
    os.environ['COGITO_PATH'] = os.path.join(os.getcwd(), 'libcogito.so')
import cogito

def handle(event, context):
    response = {
        'Status': 'SUCCESS',
        'PhysicalResourceId': event['PhysicalResourceId'],
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId']
    }

    try:
        converted = cogito.to_json(event['ResourceProperties']['Policy'])
        response['Data'] = {}
        response['Data']['Policy'] = converted
    except cogito.CogitoError as exception:
        response['Status'] = 'FAILED'
        response['Resource'] = exception.message

    requests.put(event['ResponseURL'], json.dumps(response))
    return response
