from decimal import Decimal
import boto3
import os
import simplejson as json
from datetime import datetime
import dateutil.tz

zone = dateutil.tz.gettz('US/Central')
TABLE_NAME = os.environ.get('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
today = str(datetime.now(zone).date())

def handler(event, context):
    body = json.loads(event['body'])
    user = body['user']
    activity = body['activity']
    number = Decimal(body['number'])

    
    try:
        table.update_item(
        Key = {'id': user},
        ExpressionAttributeNames={
            '#workouts': 'workouts',
            },
        ExpressionAttributeValues={':empty': {}},
        ConditionExpression= "attribute_not_exists(#workouts)",
        UpdateExpression="SET #workouts = :empty",
    )
    except:
        pass

    try:
        table.update_item(
        Key = {'id': user},
        ExpressionAttributeNames={
            '#workouts': 'workouts',
            '#dailyworkouts': today
            },
        ExpressionAttributeValues={':empty': {}},
        ConditionExpression= "attribute_not_exists(#workouts.#dailyworkouts)",
        UpdateExpression="SET #workouts.#dailyworkouts = :empty",
    )
    except:
        pass

    response = table.update_item(
    Key = {'id': user},
    ExpressionAttributeNames={
        '#activity': activity,
        '#activitytotal': activity+"total",
        '#workouts': 'workouts', 
        '#dailyworkouts': today
        },
    ExpressionAttributeValues={':numb': number},
    UpdateExpression="ADD #workouts.#dailyworkouts.#activity :numb, #activitytotal :numb",
    ReturnValues="ALL_NEW"
    )

    print(response)
    print(dir(response))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }