import boto3

client = boto3.client('s3')

response = client.create_bucket(
    Bucket='gou8m',   # must be globally unique
    CreateBucketConfiguration={
        'LocationConstraint': 'us-east-1'
    }
)

print("Bucket created successfully:", response)
