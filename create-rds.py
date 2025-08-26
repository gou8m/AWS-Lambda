import boto3

# Initialize a session using your credentials
rds_client = boto3.client('rds', region_name="ap-south-1")  # specify your region

# Parameters for the RDS instance
db_instance_identifier = 'my-rds-instance'  # must be unique per account/region
db_instance_class = 'db.t3.micro'  # small free-tier eligible instance
engine = 'mysql'  # engine type
master_username = 'admin'  
master_user_password = 'Cloud123!'  # Strong password (avoid weak ones)
allocated_storage = 20  # in GB
db_name = 'mydb'  

try:
    response = rds_client.create_db_instance(
        DBInstanceIdentifier=db_instance_identifier,
        AllocatedStorage=allocated_storage,
        DBInstanceClass=db_instance_class,
        Engine=engine,
        MasterUsername=master_username,
        MasterUserPassword=master_user_password,
        DBName=db_name,
        BackupRetentionPeriod=7,
        Port=3306,
        MultiAZ=False,
        PubliclyAccessible=True,
        StorageType='gp2',
        Tags=[
            {'Key': 'Name', 'Value': 'MyRDSInstance'}
        ]
    )
    print(f"RDS instance '{db_instance_identifier}' creation initiated.")
    print("Current Status:", response['DBInstance']['DBInstanceStatus'])

except Exception as e:
    print(f"Error creating RDS instance: {str(e)}")
