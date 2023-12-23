import logging
from botocore.exceptions import ClientError
from util.manage_connection import delete_connection

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, _):
    request_context = event.get('requestContext', {})
    connection_id = request_context.get('connectionId')
    game_id = request_context.get('gameId')
    if connection_id is None or game_id is None:
        return {'statusCode': 400}

    status_code = 200
    try:
        delete_connection(connection_id=connection_id, game_id=game_id)
        logger.debug(f"Deleted connection {connection_id} for game {game_id}")
    except ClientError:
        logger.exception(
            f"Couldn't delete connection {connection_id} for game {game_id}"
        )
        status_code = 503
    return status_code
