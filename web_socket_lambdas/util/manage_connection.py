import boto3


def add_connection(connection_id, game_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('famous-fishbowl')

    table.put_item(
        Item={
            'pk': f'gameConnection_${game_id}',
            'sk': connection_id
        }
    )