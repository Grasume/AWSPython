import boto3

accounts = []
region = []

def ebs_enable_encryption_flag(accounts, region):
    for acct in accounts:
        session = boto3.Session(profile_name=acct)
        for location in region:
            ec2client = session.client('ec2',region_name=location)
            response = ec2client.enable_ebs_encryption_by_default()
            print(acct+" "+location+" Encryption flag Set ", response['EbsEncryptionByDefault'])



ebs_enable_encryption_flag(accounts,region)
