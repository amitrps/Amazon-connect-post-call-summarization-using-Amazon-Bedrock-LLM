#!/bin/bash

# Script to package and deploy the transcript summarizer as a Lambda function

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it first."
    exit 1
fi

# Create a temporary directory for packaging
echo "Creating deployment package..."
mkdir -p deployment_package
cp transcript_summarizer.py deployment_package/
cd deployment_package

# Install dependencies in the package directory
echo "Installing dependencies..."
pip install -t . boto3

# Create the deployment ZIP
echo "Creating ZIP file..."
zip -r ../transcript_summarizer.zip .
cd ..

# Clean up
rm -rf deployment_package

echo "Deployment package created: transcript_summarizer.zip"
echo ""
echo "To deploy to Lambda, run:"
echo "aws lambda create-function \\"
echo "  --function-name connect-transcript-summarizer \\"
echo "  --runtime python3.9 \\"
echo "  --handler transcript_summarizer.lambda_handler \\"
echo "  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_LAMBDA_ROLE \\"
echo "  --zip-file fileb://transcript_summarizer.zip \\"
echo "  --timeout 60 \\"
echo "  --memory-size 256"
echo ""
echo "Or update an existing function with:"
echo "aws lambda update-function-code \\"
echo "  --function-name connect-transcript-summarizer \\"
echo "  --zip-file fileb://transcript_summarizer.zip"

# Make the script executable
chmod +x lambda_deployment.sh
