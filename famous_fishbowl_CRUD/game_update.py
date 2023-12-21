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
    status_code = 200

    try:
        id_str = event['pathParameters']['id']
        request_json = json.loads(event['body'])

        update_string = 'SET'
        expression_values = {}
        expression_names = {}
        for key, value in request_json.items():
            expression_value = ':'+key
            expression_name = '#'+key
            expression_values[expression_value] = value

            # Set lastUpdateTime to currentUpdateTime value
            if key == 'currentUpdateTime':
                expression_names[expression_name] = 'lastUpdateTime'
            else:
                expression_names[expression_name] = key

            if key != 'lastUpdateTime':
                update_string += ' ' + expression_name + ' = ' + expression_value + ','

        update_string = update_string[0:-1]

        table.update_item(
            Key={
                'pk': 'gameInstance',
                'sk': id_str
            },
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            UpdateExpression=update_string,
            ConditionExpression='attribute_not_exists(#lastUpdateTime) OR #lastUpdateTime <= :lastUpdateTime',
            ReturnValuesOnConditionCheckFailure='ALL_OLD'
        )
        body = f'Updated Game {id_str}'
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException as err:
        if 'Item' in err.response:
            item = err.response['Item']
            deserializer = boto3.dynamodb.types.TypeDeserializer()
            item = deserializer.deserialize({'M': item})
            body = json.dumps(item, use_decimal=True)
        else:
            body = f"Condition check failed: stale update"
        print(body)
        status_code = 409
    except Exception as err:
        body = f"Unexpected {err}, {type(err)}"
        print(body)
        status_code = 400

    return {
        'statusCode': status_code,
        'body': body,
        'headers': headers
    }

