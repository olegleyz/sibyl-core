import json
from datetime import datetime
from typing import Any, Dict

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

from models.user import User, UserCreate
from services.dynamodb import DynamoDBService

logger = Logger()
app = APIGatewayRestResolver()
dynamodb = DynamoDBService()

def create_response(status_code: int, body: Any) -> Dict:
    if isinstance(body, (User, UserCreate)):
        body_str = body.model_dump_json()
    else:
        body_str = json.dumps(body)
        
    return {
        'statusCode': status_code,
        'body': body_str,
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def create_user(event: Dict) -> Dict:
    """Create a new user"""
    try:
        body = json.loads(event['body'])
        user = User(
            **body,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        
        if dynamodb.put_item(user.to_dynamodb_item()):
            return create_response(201, user)
        return create_response(500, {'error': 'Failed to create user'})
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return create_response(400, {'error': str(e)})

def get_user_by_telegram_id(event: Dict) -> Dict:
    """Get a user by telegram_id"""
    try:
        telegram_id = event['pathParameters']['telegram_id']
        item = dynamodb.get_item_by_telegram_id(telegram_id)
        
        if not item:
            return create_response(404, {'error': 'User not found'})
            
        user = User.from_dynamodb_item(item)
        return create_response(200, user)
    except Exception as e:
        logger.error(f"Error getting user by telegram_id: {str(e)}")
        return create_response(400, {'error': str(e)})

def get_user_by_id(event: Dict) -> Dict:
    """Get a user by UUID"""
    try:
        user_id = event['pathParameters']['id']
        item = dynamodb.get_item_by_uuid(user_id)
        
        if not item:
            return create_response(404, {'error': 'User not found'})
            
        user = User.from_dynamodb_item(item)
        return create_response(200, user)
    except Exception as e:
        logger.error(f"Error getting user by UUID: {str(e)}")
        return create_response(400, {'error': str(e)})

def update_user(event: Dict) -> Dict:
    """Update a user by UUID"""
    try:
        user_id = event['pathParameters']['id']
        body = json.loads(event['body'])
        
        # Check if user exists
        existing_item = dynamodb.get_item_by_uuid(user_id)
        if not existing_item:
            return create_response(404, {'error': 'User not found'})
            
        # Create updated user
        user = User.from_dynamodb_item(existing_item)
        update_data = {
            **body,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        if dynamodb.update_item(user.uuid, update_data):
            updated_item = dynamodb.get_item_by_uuid(user.uuid)
            updated_user = User.from_dynamodb_item(updated_item)
            return create_response(200, updated_user)
        return create_response(500, {'error': 'Failed to update user'})
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        return create_response(400, {'error': str(e)})

def update_user_by_telegram_id(event: Dict) -> Dict:
    """Update a user by telegram_id"""
    try:
        telegram_id = event['pathParameters']['telegram_id']
        body = json.loads(event['body'])
        
        # Find user by telegram_id
        existing_user = dynamodb.get_item_by_telegram_id(telegram_id)
        if not existing_user:
            return create_response(404, {'error': 'User not found'})
        
        user = User.from_dynamodb_item(existing_user)
        update_data = {**body, 'updated_at': datetime.utcnow().isoformat()}
        
        if dynamodb.update_item(user.uuid, update_data):
            updated_item = dynamodb.get_item_by_uuid(user.uuid)
            updated_user = User.from_dynamodb_item(updated_item)
            return create_response(200, updated_user)
        return create_response(500, {'error': 'Failed to update user'})
    except Exception as e:
        logger.error(f"Error updating user by telegram_id: {str(e)}")
        return create_response(400, {'error': str(e)})

def delete_user(event: Dict) -> Dict:
    """Delete a user by UUID"""
    try:
        user_id = event['pathParameters']['id']
        
        if dynamodb.delete_item(user_id):
            return create_response(204, {})
        return create_response(500, {'error': 'Failed to delete user'})
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        return create_response(400, {'error': str(e)})

def handler(event: Dict, context: LambdaContext) -> Dict:
    """Main handler for all user CRUD operations"""
    try:
        http_method = event['httpMethod']
        path = event['path']
        
        if http_method == 'POST' and path == '/users':
            return create_user(event)
        elif http_method == 'GET':
            if '/users/telegram/' in path:
                return get_user_by_telegram_id(event)
            elif '/users/' in path:
                return get_user_by_id(event)
        elif http_method == 'PUT':
            if '/users/telegram/' in path:
                return update_user_by_telegram_id(event)
            elif '/users/' in path:
                return update_user(event)
        elif http_method == 'DELETE' and '/users/' in path:
            return delete_user(event)
        else:
            return create_response(404, {'error': 'Not found'})
    except Exception as e:
        logger.error(f"Error in handler: {str(e)}")
        return create_response(500, {'error': 'Internal server error'})
