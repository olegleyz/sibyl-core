# Sibyl Core Service

Core backend service for [Sibyl Numerology Bot](https://meet-sibyl.com), providing REST APIs for user management and AI agent interactions.

## Overview

This service is built using AWS SAM (Serverless Application Model) and provides the following functionalities:
- User profile management
- Integration with Telegram interface
- Access control for AI agents
- Multi-environment support (dev/prod)

## Architecture

The service uses the following AWS services:
- API Gateway for REST endpoints
- Lambda for serverless compute
- DynamoDB for data storage
- IAM for access control
- CloudFormation for infrastructure as code

## API Endpoints

### Users
- `POST /users` - Create a new user
- `GET /users/{id}` - Get user by UUID
- `PUT /users/{id}` - Update user by UUID
- `GET /users/telegram/{telegram_id}` - Get user by Telegram ID
- `PUT /users/telegram/{telegram_id}` - Update user by Telegram ID

## Security

The API is secured using:
- Resource-based policies for API Gateway
- Environment-specific access controls
- IAM role-based authentication

## Development

### Prerequisites
- AWS SAM CLI
- Python 3.9+
- AWS credentials configured

### Local Development
```bash
# Install dependencies
pip install -r src/requirements.txt

# Start local API
sam local start-api

# Run tests
python -m pytest tests/
```

### Deployment
```bash
# Deploy to dev
sam deploy --config-env dev

# Deploy to prod
sam deploy --config-env prod
```

## Environment Variables
- `ENVIRONMENT` - Deployment environment (dev/prod)
- `TABLE_NAME` - DynamoDB table name

## Contributing
Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Create a pull request

## License
Proprietary - All rights reserved
