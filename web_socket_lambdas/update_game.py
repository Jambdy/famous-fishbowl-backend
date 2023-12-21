import logging
import json
from util.manage_connection import add_connection, send_to_connections
from util.manage_game import create_game, add_names

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, _):
    request_context = event.get('requestContext', {})
    connection_id = request_context.get('connectionId')
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
        domain_name = request_context.get('domainName', '')
        stage = request_context.get('stage', '')
        endpoint_url = f"https://{domain_name}/{stage}"

        if game_action == 'createGame':
            create_game(game)
            add_connection(connection_id, game_id)
        elif game_action == 'joinGame':
            add_connection(connection_id, game_id)
        elif game_action == 'addNames':
            add_names(game_id, game)
            send_to_connections(endpoint_url, connection_id, game)
        elif game_action == 'updateGame':
            send_to_connections(endpoint_url, connection_id, {'test':'tester'})
        else:
            logger.exception(
                f'Invalid game action: {game_action}'
            )
            status_code = 500

    except Exception as err:
        logger.exception(f'Unexpected {err}, {type(err)}')
        status_code = 500

    return {'statusCode': status_code}
