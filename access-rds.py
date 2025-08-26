import os
import pymysql

# Database settings from environment variables
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
new_db_name = "test"   # Change as needed
table_name = "mytable" # Change as needed

# Establish a database connection
def connect_to_rds():
    return pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5
    )

# Lambda function handler
def lambda_handler(event, context):
    connection = None
    try:
        connection = connect_to_rds()
        with connection.cursor() as cursor:
            # Create a new database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{new_db_name}`;")

            # Select the new database
            cursor.execute(f"USE `{new_db_name}`;")

            # Create a new table
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS `{table_name}` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            connection.commit()

            print(f"Database '{new_db_name}' and table '{table_name}' created successfully.")
            return {
                'statusCode': 200,
                'body': f"Database '{new_db_name}' and table '{table_name}' created successfully."
            }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }
    finally:
        if connection:
            connection.close()
