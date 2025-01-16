.PHONY: build deploy clean install install-swagger install-python

# Default values
REGION ?= us-east-1

# Default target
all: build deploy

# Install all dependencies
install: install-swagger install-python

# Install Swagger CLI
install-swagger:
	npm install -g @apidevtools/swagger-cli

# Install Python dependencies
install-python:
	pip install -r src/requirements.txt

# Build OpenAPI spec
build-api:
	swagger-cli bundle -o model/api/openapi.yaml --dereference --t yaml model/api/apiSkeleton.yaml
	swagger-cli validate model/api/openapi.yaml

# Build SAM template
build: build-api
	sam validate --region $(REGION)
	sam build --parallel

# Deploy
deploy:
	sam deploy --region $(REGION) --profile admin

# Clean build artifacts
clean:
	rm -f model/api/openapi.yaml
	rm -rf .aws-sam
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
