import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, _):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('famous-fishbowl')

    connection_id = event.get('requestContext', {}).get('connectionId')
    body = event.get('requestContext', {}).get('body')
    if connection_id is None:
        return {'statusCode': 400}

    status_code = 200
    try:
        logger.debug(f"Received {body}")
    except ClientError:
        logger.exception(
            f"Couldn't log for {connection_id}"
        )
        status_code = 500
    return status_code