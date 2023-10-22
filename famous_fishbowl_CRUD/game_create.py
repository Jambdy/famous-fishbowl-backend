import simplejson as json
import boto3


def lambda_handler(event, _):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('famous-fishbowl')
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST',
        'Access-Control-Allow-Credentials': True
    }
    body = ''
    status_code = 200

    try:
        request_json = json.loads(event['body'])
        table.put_item(
            Item={
                'pk': 'gameInstance',
                'sk': request_json['id'],
                'state': request_json['state'],
                'creationTime': request_json['creationTime'],
                'categories': request_json['categories'],
                'names': request_json['names'],
                'round': request_json['round'],
                'curTeam': request_json['curTeam'],
                'teamScores': request_json['teamScores'],
                'lastUpdateTime': request_json['lastUpdateTime']
            }
        )
        body = f'Created Game {request_json["id"]}'
    except Exception as err:
        body = f"Unexpected {err}, {type(err)}"
        print(body)
        status_code = 400

    return {
        'statusCode': status_code,
        'body': body,
        'headers': headers
    }

