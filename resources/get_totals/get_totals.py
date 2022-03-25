import boto3
import os
from datetime import datetime
import simplejson as json

TABLE_NAME = os.environ.get('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def handler(event, context):
    body = json.loads(event['body'])
    user = body['user']

    response = table.get_item(Key={'id': user})

    response['Item']['retrieved_date'] = str(datetime.now())
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response['Item'])
    }