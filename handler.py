import os
os.environ['COGITO_PATH'] = os.path.join(os.getcwd(), 'libcogito.so')
import cogito

def handle(event, context):
    return cogito.to_json(event['IAM'])
