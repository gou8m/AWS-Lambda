import boto3

def lambda_handler(event, context):
    try:
        ec2 = boto3.client("ec2")

        response = ec2.run_instances(
            ImageId="ami-001843b876406202a",  # ✅ replace with valid AMI in your region
            InstanceType="t2.micro",
            KeyName="test",  # ✅ must exist in the same region
            MinCount=1,
            MaxCount=1
        )

        instance_id = response["Instances"][0]["InstanceId"]

        return {
            "statusCode": 200,
            "body": f"EC2 Instance launched successfully: {instance_id}"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
