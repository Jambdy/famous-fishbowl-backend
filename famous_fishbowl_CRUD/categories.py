import simplejson as json
import boto3
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, _):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('famous-fishbowl')
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,GET',
        'Access-Control-Allow-Credentials': True
    }
    body = ''
    status_code = 200

    try:
        response = table.query(
            KeyConditionExpression = Key('id').eq('category')
        )
        if 'Items' in response:
            items = response['Items']
            body = json.dumps(items, use_decimal=True)
        else:
            status_code = 404
            body = f'No categories found'
    except Exception as err:
        body = f"Unexpected {err}, {type(err)}"
        print(body)
        status_code = 400

    return {
        'statusCode': status_code,
        'body': body,
        'headers': headers
    }
