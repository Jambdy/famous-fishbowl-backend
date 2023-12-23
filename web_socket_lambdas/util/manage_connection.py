import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import logging
import simplejson as json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('famous-fishbowl')


def add_connection(connection_id, game_id):
    table.put_item(
        Item={
            'pk': f'gameConnection_{game_id}',
            'sk': connection_id
        }
    )


def delete_connection(connection_id, game_id):
    table.delete_item(
        Key={
            'pk': f'gameConnection_{game_id}',
            'sk': connection_id
        }
    )

def send_to_connections(endpoint_url, game_id, origin_connection_id, data, return_to_sender=False):
    # Get non-origin connections to send ids to
    pk = f'gameConnection_{game_id}'
    key_condition_expression = Key('pk').eq(pk)
    response = table.query(
        KeyConditionExpression=key_condition_expression,
    )
    connection_ids = [item.get('sk', '') for item in response.get('Items', {})]

    api_management_client = boto3.client(
        'apigatewaymanagementapi', endpoint_url=endpoint_url
    )

    for connection_id in connection_ids:
        if (return_to_sender and connection_id == origin_connection_id) or (
                not return_to_sender and connection_id != origin_connection_id):
            try:
                send_response = api_management_client.post_to_connection(
                    Data=json.dumps(data, use_decimal=True), ConnectionId=connection_id
                )
                logger.debug(
                    "Posted message to connection %s, got response %s.",
                    connection_id,
                    send_response,
                )
            except api_management_client.exceptions.GoneException:
                logger.info("Connection %s is gone, removing.", connection_id)
                try:
                    table.delete_item(Key={'pk': pk, 'sk': connection_id})
                except ClientError:
                    logger.exception("Couldn't remove connection %s.", connection_id)

            except ClientError:
                logger.exception("Couldn't post to connection %s.", connection_id)
