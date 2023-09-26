import simplejson as json
import boto3


def lambda_handler(event, _):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('famous-fishbowl')
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,PUT,GET,DELETE',
        'Access-Control-Allow-Credentials': True
    }
    body = ''
    status_code = 200

    try:
        if event['httpMethod'] == 'DELETE':
            id_str = event['pathParameters']['id']
            table.delete_item(
                Key={
                    'id': id_str
                }
            )
            body = f'Deleted item {id_str}'
        elif event['httpMethod'] == 'GET':
            id_str = event['pathParameters']['id']
            response = table.get_item(
                Key={
                    'id': id_str
                }
            )
            if 'Item' in response:
                item = response['Item']
                body = json.dumps(item, use_decimal=True)
            else:
                status_code = 404
                body = f'Game {id_str} not found'
        elif event['httpMethod'] == 'PUT':
            request_json = json.loads(event['body'])
            table.put_item(
                Item={
                    'id': request_json['id'],
                    'state': request_json['state'],
                    'creationTime': request_json['creationTime'],
                    'completionTime': request_json['completionTime'],
                    'categories': request_json['categories'],
                    'names': request_json['names'],
                    'round': request_json['round'],
                    'curTeam': request_json['curTeam'],
                    'teamScores': request_json['teamScores'],
                    'timeRemaining': request_json['timeRemaining'],
                    'turnResumeTime': request_json['turnResumeTime']
                }
            )
            body = f'Put Game {request_json["id"]}'
    except Exception as err:
        body = f"Unexpected {err}, {type(err)}"
        print(body)
        status_code = 400

    return {
        'statusCode': status_code,
        'body': body,
        'headers': headers
    }
