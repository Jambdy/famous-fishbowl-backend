import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('famous-fishbowl')


def add_connection(connection_id, game_id):
    table.put_item(
        Item={
            'pk': f'gameConnection_{game_id}',
            'sk': connection_id
        }
    )
