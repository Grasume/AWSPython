import boto3

accounts = []
region = []


def Rds_Encryption_Check(accounts,region):
    for acct in accounts:
        session = boto3.Session(profile_name=acct)
        for location in region:
            rdsclient = session.client('rds',region_name=location)
            rdsResponse = rdsclient.describe_db_instances()

            for rds in rdsResponse['DBInstances']:
                if rds['StorageEncrypted'] == False:
                    print('RDS Instance ' + rds['DBInstanceIdentifier'] + ' Encryption Status ' + str(rds['StorageEncrypted']))


Rds_Encryption_Check(accounts,region)
