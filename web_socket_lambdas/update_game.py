import logging
import boto3
from botocore.exceptions import ClientError
from util.manage_connection import add_connection

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, _):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('famous-fishbowl')

    connection_id = event.get('requestContext', {}).get('connectionId')
    if connection_id is None:
        return {'statusCode': 400}

    body = event.get('body', {})
    logger.debug(f'Received: {body}')
    game_action = body.get('game_action')

    status_code = 200
    try:
        game_id = body.get('gameId', '')
        if game_action == 'createGame':
            add_connection(connection_id, game_id)
        elif game_action == 'joinGame':
            add_connection(connection_id, game_id)
        elif game_action == 'updateGame':
            print('placeholder')
        else:
            logger.exception(
                f'Invalid game action: {game_action}'
            )
            status_code = 500

    except ClientError:
        logger.exception(
            f'Error during {game_action}'
        )
        status_code = 500

    return {'statusCode': status_code}
