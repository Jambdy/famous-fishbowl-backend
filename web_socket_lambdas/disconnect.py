import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, _):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('famous-fishbowl')

    connection_id = event.get('requestContext', {}).get('connectionId')
    if connection_id is None:
        return {'statusCode': 400}

    status_code = 200
    try:
        table.delete_item(
            Key={
                'pk': 'socketConnection',
                'sk': connection_id
            }
        )
        logger.debug(f"Deleted connection {connection_id}")
    except ClientError:
        logger.exception(
            f"Couldn't delete connection {connection_id}"
        )
        status_code = 503
    return status_code
