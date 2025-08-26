import boto3
import json
import os
from datetime import datetime

# Get CloudFront Distribution ID from environment variables
CLOUDFRONT_DISTRIBUTION_ID = os.environ.get("CLOUDFRONT_DISTRIBUTION_ID", "")

cloudfront_client = boto3.client("cloudfront")

def lambda_handler(event, context):
    try:
        # Use event paths if provided, else default to all
        paths = event.get("paths", ["/*"])

        response = cloudfront_client.create_invalidation(
            DistributionId=CLOUDFRONT_DISTRIBUTION_ID,
            InvalidationBatch={
                "Paths": {
                    "Quantity": len(paths),
                    "Items": paths
                },
                "CallerReference": str(datetime.utcnow().timestamp())
            }
        )

        invalidation_id = response["Invalidation"]["Id"]
        create_time = response["Invalidation"]["CreateTime"].isoformat()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Invalidation request sent successfully",
                "InvalidationId": invalidation_id,
                "CreateTime": create_time
            })
        }

    except Exception as e:
        print(f"Error creating invalidation: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Failed to create invalidation",
                "message": str(e)
            })
        }
