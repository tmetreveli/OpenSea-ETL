import boto3
import json

# Specify AWS access keys directly in code
aws_access_key_id = 'AKIA3FLDXATPRWR33NE7'
aws_secret_access_key = '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'

# Initialize Boto3 S3 client with the specified credentials
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Bucket name and object key
bucket_name = 'openseacollections'


async def uploadS3(data, filename):
    try:
        # Convert Python dictionary to JSON string
        json_data = json.dumps(data)

        # Upload JSON object to S3
        s3.put_object(Body=json_data, Bucket=bucket_name, Key=filename)

    except:
        print('Can not upload to S3 Bucket')

print("JSON object uploaded successfully to S3.")
