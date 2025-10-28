#!/bin/bash
set -eo pipefail

# Define the directory for the deployment package
DEPLOY_DIR="wisita_lambda_package"
mkdir -p "$DEPLOY_DIR"

# 1. Install Dependencies Locally (Requires your current directory to match Lambda's environment)
# NOTE: If using an AWS Layer for requests, you can skip this 'pip install requests' step.
# For simplicity and robustness if you're not using a layer, we'll include requests here.

echo "Installing requests library into deployment package..."
pip install requests -t "$DEPLOY_DIR"

# 2. Copy the Lambda handler code into the package root
cp ../../src/lambda_function.py "$DEPLOY_DIR"/

# 3. Create the deployment zip file
DEPLOYMENT_ZIP="wistia_lambda_package.zip"

echo "Creating deployment package: $DEPLOYMENT_ZIP"
cd "$DEPLOY_DIR"
zip -r "../$DEPLOYMENT_ZIP" .

# Clean up temporary directory
cd ..
rm -rf "$DEPLOY_DIR"

echo "Package creation complete. Ready to deploy $DEPLOYMENT_ZIP"
