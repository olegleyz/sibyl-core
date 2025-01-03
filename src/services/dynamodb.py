import os
import boto3
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger

logger = Logger()

class DynamoDBService:
    def __init__(self):
        self.table_name = os.environ['TABLE_NAME']
        self.gsi_name = f"TelegramIdIndex-{os.environ['ENVIRONMENT']}"
        self.table = boto3.resource('dynamodb').Table(self.table_name)

    def put_item(self, item: dict) -> bool:
        try:
            self.table.put_item(Item=item)
            return True
        except ClientError as e:
            logger.error(f"Error putting item: {str(e)}")
            return False

    def get_item_by_uuid(self, uuid: str) -> dict:
        try:
            response = self.table.get_item(Key={'uuid': uuid})
            return response.get('Item')
        except ClientError as e:
            logger.error(f"Error getting item by UUID: {str(e)}")
            return None

    def get_item_by_telegram_id(self, telegram_id: str) -> dict:
        try:
            response = self.table.query(
                IndexName=self.gsi_name,
                KeyConditionExpression='telegram_id = :tid',
                ExpressionAttributeValues={':tid': telegram_id}
            )
            items = response.get('Items', [])
            return items[0] if items else None
        except ClientError as e:
            logger.error(f"Error getting item by telegram_id: {str(e)}")
            return None

    def update_item(self, uuid: str, update_data: dict) -> bool:
        update_expression = []
        expression_attribute_values = {}
        expression_attribute_names = {}

        for key, value in update_data.items():
            if value is not None:
                update_expression.append(f"#{key} = :{key}")
                expression_attribute_values[f":{key}"] = value
                expression_attribute_names[f"#{key}"] = key

        if not update_expression:
            return True

        try:
            self.table.update_item(
                Key={'uuid': uuid},
                UpdateExpression=f"SET {', '.join(update_expression)}",
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names
            )
            return True
        except ClientError as e:
            logger.error(f"Error updating item: {str(e)}")
            return False

    def delete_item(self, uuid: str) -> bool:
        try:
            self.table.delete_item(Key={'uuid': uuid})
            return True
        except ClientError as e:
            logger.error(f"Error deleting item: {str(e)}")
            return False
