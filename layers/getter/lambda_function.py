import boto3
import logging
import simplejson as json

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level = logging.INFO, force=True)


dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table("tf_rpiTracker") # TODO: Make it not hardcoded

def lambda_handler(event,context):
    res=table.scan()
    logging.debug(res['Items'])
    return {
        'statusCode': '200',
        'body':json.dumps(res['Items']),
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        }
    }