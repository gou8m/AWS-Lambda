import json
import boto3
import pymysql

# Define DB and table
new_db_name = "test"
table_name = "mytable"

# Get RDS credentials from AWS Secrets Manager
def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Connect to RDS
def connect_to_rds(secret):
    return pymysql.connect(
        host=secret['host'],
        user=secret['username'],
        password=secret['password'],
        port=int(secret.get('port', 3306)),  # Default MySQL port
        cursorclass=pymysql.cursors.DictCursor
    )

# Lambda handler
def lambda_handler(event, context):
    secret_name = "my_secret"  # ✅ replace with your secret name in Secrets Manager
    
    try:
        secret = get_secret(secret_name)
        connection = connect_to_rds(secret)
        
        with connection.cursor() as cursor:
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name};")
            cursor.execute(f"USE {new_db_name};")

            # Create table if not exists
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
        
        connection.commit()

        return {
            'statusCode': 200,
            'body': f"✅ Database '{new_db_name}' and table '{table_name}' created successfully."
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }

    finally:
        if 'connection' in locals():
            connection.close()
