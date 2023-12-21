import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('famous-fishbowl')


def create_game(game_json):
    try:
        table.put_item(
            Item={
                'pk': 'gameInstance',
                'sk': game_json.get('id', ''),
                'gameState': game_json.get('gameState', ''),
                'creationTime': game_json.get('creationTime', ''),
                'categories': game_json.get('categories', ''),
                'names': game_json.get('names', ''),
                'round': game_json.get('round', ''),
                'curTeam': game_json.get('curTeam', ''),
                'teamScores': game_json.get('teamScores', ''),
                'lastUpdateTime': game_json.get('lastUpdateTime', '')
            }
        )
        logger.debug(f'Created Game {game_json["id"]}')
    except Exception as err:
        logger.exception(f'Error during create: unexpected {err}, {type(err)}')


def add_names(game_id, game_json):
    try:
        update_string = 'SET #names = list_append(#names, :names)'
        expression_values = {
            ':names': game_json['names']
        }
        expression_names = {
            '#names': 'names'
        }

        response = table.update_item(
            Key={
                'pk': 'gameInstance',
                'sk': game_id
            },
            UpdateExpression=update_string,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ReturnValues='ALL_NEW'
        )
        logger.debug(f'Added Names to Game {game_id}')
        return response.get('Attributes')
    except Exception as err:
        logger.exception(f'Error during add names: unexpected {err}, {type(err)}')
