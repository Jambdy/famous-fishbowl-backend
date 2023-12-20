import logging
import json
from util.manage_connection import add_connection
from util.manage_game import create_game

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, _):
    connection_id = event.get('requestContext', {}).get('connectionId')
    if connection_id is None:
        return {'statusCode': 400}

    body = event.get('body', {})
    logger.debug(f'Received: {body}')

    status_code = 200
    try:
        body = json.loads(body)
        game_action = body.get('gameAction', '')
        game_id = body.get('gameId', '')
        game = body.get('game', '')

        if game_action == 'createGame':
            create_game(game)
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

    except Exception as err:
        logger.exception(f'Unexpected {err}, {type(err)}')
        status_code = 500

    return {'statusCode': status_code}
