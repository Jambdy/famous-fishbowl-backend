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
