import os
from pathlib import Path
import subprocess
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
ZIP_FILE = "lambda_function.zip"
FUNCTION_NAME = os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def update_lambda():
    """Upload lambda_function.zip to AWS Lambda"""
    
    # Validate environment variables
    if not FUNCTION_NAME:
        raise ValueError("AWS_LAMBDA_FUNCTION_NAME not found in .env file")
    
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) not found in .env file")


    # Execute build_lambda.sh script
    print("Executing build_lambda.sh...")
    try:
        subprocess.run(["bash", "build_lambda.sh"], check=True, cwd=Path(__file__).parent)
        print("✓ Successfully built lambda package")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to execute build_lambda.sh: {e}")

    # Check if the zip file exists
    zip_path = Path(ZIP_FILE)
    if not zip_path.exists():
        raise FileNotFoundError(f"{ZIP_FILE} not found. Run build_lambda.sh first.")
    
    print(f"Uploading {ZIP_FILE} to Lambda function: {FUNCTION_NAME}")
    print(f"Region: {AWS_REGION}")
    
    # Create Lambda client
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    
    # Read the zip file
    with open(zip_path, 'rb') as f:
        zip_content = f.read()
    
    # Upload to Lambda
    try:
        response = lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            ZipFile=zip_content
        )
        
        print(f"✓ Successfully updated Lambda function")
        print(f"  Function ARN: {response['FunctionArn']}")
        print(f"  Runtime: {response['Runtime']}")
        print(f"  Last Modified: {response['LastModified']}")
        print(f"  Code Size: {response['CodeSize']} bytes")
        
    except Exception as e:
        print(f"✗ Error updating Lambda function: {e}")
        raise


if __name__ == "__main__":
    update_lambda()
