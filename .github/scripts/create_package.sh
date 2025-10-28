#!/bin/bash
set -eo pipefail

# Define the directory for the deployment package
DEPLOY_DIR="wisita_lambda_package"
mkdir -p "$DEPLOY_DIR"

echo "Installing requests library into deployment package..."
pip install requests -t "$DEPLOY_DIR"

# Copy the Lambda handler code into the package root
cp ./src/lambda_function.py "$DEPLOY_DIR"/

# Create the deployment zip file
DEPLOYMENT_ZIP="wistia_lambda_package.zip"

echo "Creating deployment package: $DEPLOYMENT_ZIP"
cd "$DEPLOY_DIR"
zip -r "../$DEPLOYMENT_ZIP" .

cd ..
rm -rf "$DEPLOY_DIR"

echo "Package creation complete. Ready to deploy $DEPLOYMENT_ZIP"
