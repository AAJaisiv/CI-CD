#!/bin/bash

# Lambda Deployment Script
# This script packages and deploys the Lambda function to AWS

set -e

echo "🚀 Starting Lambda deployment..."

# Configuration
LAMBDA_FUNCTION_NAME="data-processor"
LAMBDA_ROLE_ARN="arn:aws:iam::872515279539:role/ci-cd-portfolio-dev-lambda-role"
LAMBDA_DIR="src/lambda/data_processor"
PACKAGE_DIR="lambda_package"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📦 Creating deployment package...${NC}"

# Clean up previous package
rm -rf $PACKAGE_DIR
mkdir -p $PACKAGE_DIR

# Copy Lambda function
cp $LAMBDA_DIR/lambda_function.py $PACKAGE_DIR/

# Install only essential dependencies
pip install boto3==1.34.0 -t $PACKAGE_DIR/

# Remove unnecessary files to reduce package size
find $PACKAGE_DIR -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find $PACKAGE_DIR -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find $PACKAGE_DIR -type d -name "*.pyc" -delete 2>/dev/null || true
find $PACKAGE_DIR -type f -name "*.pyo" -delete 2>/dev/null || true

# Create deployment package
cd $PACKAGE_DIR
zip -r ../lambda_deployment.zip . -x "*.pyc" "*/tests/*" "*/__pycache__/*"
cd ..

echo -e "${GREEN}✅ Deployment package created: lambda_deployment.zip${NC}"

# Check package size
PACKAGE_SIZE=$(stat -f%z lambda_deployment.zip 2>/dev/null || stat -c%s lambda_deployment.zip 2>/dev/null || echo "unknown")
echo -e "${YELLOW}📦 Package size: ${PACKAGE_SIZE} bytes${NC}"

# Check if Lambda function exists
echo -e "${YELLOW}🔍 Checking if Lambda function exists...${NC}"
if aws lambda get-function --function-name $LAMBDA_FUNCTION_NAME >/dev/null 2>&1; then
    echo -e "${YELLOW}📝 Updating existing Lambda function...${NC}"
    aws lambda update-function-code \
        --function-name $LAMBDA_FUNCTION_NAME \
        --zip-file fileb://lambda_deployment.zip
    
    echo -e "${GREEN}✅ Lambda function updated successfully!${NC}"
else
    echo -e "${YELLOW}🆕 Creating new Lambda function...${NC}"
    aws lambda create-function \
        --function-name $LAMBDA_FUNCTION_NAME \
        --runtime python3.11 \
        --role $LAMBDA_ROLE_ARN \
        --handler lambda_function.lambda_handler \
        --zip-file fileb://lambda_deployment.zip \
        --timeout 300 \
        --memory-size 512 \
        --environment 'Variables={BUCKET_NAME=ci-cd-portfolio-dev-data}'
    
    echo -e "${GREEN}✅ Lambda function created successfully!${NC}"
fi

# Clean up
rm -rf $PACKAGE_DIR lambda_deployment.zip

echo -e "${GREEN}🎉 Lambda deployment completed successfully!${NC}"
echo -e "${YELLOW}📋 Function details:${NC}"
echo "   Function Name: $LAMBDA_FUNCTION_NAME"
echo "   Role ARN: $LAMBDA_ROLE_ARN"
echo "   Runtime: python3.11"
echo "   Handler: lambda_function.lambda_handler" 