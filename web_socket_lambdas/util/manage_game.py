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


def update_game(game_id, game_json):
    try:
        update_string = 'SET'
        expression_values = {}
        expression_names = {}
        for key, value in game_json.items():
            expression_value = ':' + key
            expression_name = '#' + key
            expression_values[expression_value] = value

            # Set lastUpdateTime to currentUpdateTime value
            if key == 'currentUpdateTime':
                expression_names[expression_name] = 'lastUpdateTime'
            else:
                expression_names[expression_name] = key

            if key != 'lastUpdateTime':
                update_string += ' ' + expression_name + ' = ' + expression_value + ','

        update_string = update_string[0:-1]

        response = table.update_item(
            Key={
                'pk': 'gameInstance',
                'sk': game_id
            },
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            UpdateExpression=update_string,
            ReturnValues='ALL_NEW',
            ConditionExpression='attribute_not_exists(#lastUpdateTime) OR #lastUpdateTime <= :lastUpdateTime',
            ReturnValuesOnConditionCheckFailure='ALL_OLD'
        )
        logger.debug(f'Updated Game {game_id}')
        return [response.get('Attributes'), False]
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException as err:
        logger.exception(f'Stale update for Game {game_id}')
        return [err.response.get('Item'), True]
    except Exception as err:
        logger.exception(f'Error during update for Game {game_id}, Unexpected {err}, {type(err)}')
