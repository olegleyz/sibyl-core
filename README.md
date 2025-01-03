# Sibyl Core

Backend service for the Sibyl Numerology Bot, built with AWS SAM (Serverless Application Model).

## Project Structure

```
sibyl-core/
├── model/                    # Infrastructure as Code
│   ├── api/                  # OpenAPI Specification
│   │   ├── apiSkeleton.yaml  # Main OpenAPI spec file
│   │   ├── paths/           # API endpoint definitions
│   │   │   └── users/       # User-related endpoints
│   │   ├── schemas/         # API schemas
│   │   └── openapi.yaml     # Generated OpenAPI spec
│   └── templates/           # CloudFormation templates
│       ├── api.yaml         # API Gateway configuration
│       ├── database.yaml    # DynamoDB tables
│       └── lambda.yaml      # Lambda functions
├── src/                     # Python source code
│   ├── handlers/           # Lambda handlers
│   ├── models/            # Data models
│   ├── services/          # Service layer
│   └── requirements.txt   # Python dependencies
├── template.yaml           # Main SAM template
├── samconfig.toml         # SAM configuration
└── Makefile              # Build and deployment commands
```

## Features

- User Management API with CRUD operations
- AWS IAM Authentication
- DynamoDB for data storage
- Structured OpenAPI specification
- Modular CloudFormation templates

## Prerequisites

- AWS CLI configured with appropriate credentials
- Node.js and npm (for Swagger CLI)
- Python 3.12
- AWS SAM CLI

## Setup

1. Install dependencies:
```bash
make install
```

This will:
- Install Swagger CLI for OpenAPI bundling
- Install Python dependencies

## Development

The project uses a modular approach:
- OpenAPI specification is split into multiple files for better maintainability
- CloudFormation templates are separated by resource type
- Python code is organized by functionality

### API Documentation

The API specification is defined in `model/api/apiSkeleton.yaml` and related files. The bundled specification is generated during build.

### Authentication

All API endpoints use AWS IAM authentication. Access is controlled through IAM policies.

## Building and Deployment

1. Build the project:
```bash
make build
```

This will:
- Bundle the OpenAPI specification
- Validate the SAM template
- Build the Lambda functions

2. Deploy to AWS:
```bash
make deploy REGION=us-east-1
```

## Clean Up

Remove build artifacts:
```bash
make clean
```

This will remove:
- Generated OpenAPI specification
- SAM build artifacts
- Python cache files

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

[Add your license information here]
