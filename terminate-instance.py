import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.terminate_instances(
            InstanceIds=['i-0bed5ca3df3cd326e']  # ✅ replace with your instance ID(s)
        )

        return {
            "statusCode": 200,
            "body": f"Termination initiated for instance(s): {response['TerminatingInstances']}"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
