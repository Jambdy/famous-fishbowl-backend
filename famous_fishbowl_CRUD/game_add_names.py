import simplejson as json
import boto3


def lambda_handler(event, _):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('famous-fishbowl')
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,PUT',
        'Access-Control-Allow-Credentials': True
    }
    body = ''
    status_code = 200

    try:
        id_str = event['pathParameters']['id']
        request_json = json.loads(event['body'])

        update_string = 'SET #names = list_append(#names, :names)'
        expression_values = {
            ':names': request_json['names']
        }
        expression_names = {
            '#names': 'names'
        }

        table.update_item(
            Key={
                'pk': 'gameInstance',
                'sk': id_str
            },
            UpdateExpression=update_string,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values
        )
        body = f'Added Names to Game {id_str}'
    except Exception as err:
        body = f"Unexpected {err}, {type(err)}"
        print(body)
        status_code = 400

    return {
        'statusCode': status_code,
        'body': body,
        'headers': headers
    }

