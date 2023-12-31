import simplejson as json
import boto3


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
        id_str = event['pathParameters']['id']
        response = table.get_item(
            Key={
                'pk': 'gameInstance',
                'sk': id_str
            }
        )
        if 'Item' in response:
            item = response['Item']
            body = json.dumps(item, use_decimal=True)
        else:
            status_code = 404
            body = f'Game {id_str} not found'
    except Exception as err:
        body = f"Unexpected {err}, {type(err)}"
        print(body)
        status_code = 400

    return {
        'statusCode': status_code,
        'body': body,
        'headers': headers
    }
