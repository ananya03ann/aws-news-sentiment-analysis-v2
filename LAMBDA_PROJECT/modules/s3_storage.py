import boto3
import json

s3 = boto3.client("s3")

def upload_to_s3(bucket_name, file_name, data):

    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(data)
    )