import boto3

# Setup Connection
rds = boto3.client('rds')

#####################################
# List RDS Instances
#####################################
try:
    dbs = rds.describe_db_instances()

for db in dbs['DBInstances']:
    print("%s@%s:%s %s") % (
        db['MasterUsername'],
        db['Endpoint']['Address'],
        db['Endpoint']['Port'],
        db['DBInstanceStatus'])
except Exception as e:
    print(e)


#####################################
# Create RDS Instance
#####################################
try:
    response = rds.create_db_instance(
        DBInstanceIdentifier='dbserver',
        MasterUsername='dbadmin',
        MasterUserPassword='abcdefg123456789',
        DBInstanceClass='db.t2.micro',
        Engine='mariadb',
        AllocatedStorage=5)
    print(response)
except Exception as e:
    print(e)


#####################################
# Delete RDS Instance
#####################################
db = sys.argv[1]
rds = boto3.client('rds')
try:
    response = rds.delete_db_instance(
        DBInstanceIdentifier=db,
        SkipFinalSnapshot=True)
    print(response)
except Exception as e:
    print(error)
