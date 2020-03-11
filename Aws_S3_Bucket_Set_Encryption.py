import boto3

accounts = ['Unmanaged']
region = ['us-east-1','us-east-2','ap-south-1','ap-northeast-1','ap-southeast-1','ap-northeast-2','ap-southeast-2','ca-central-1','eu-central-1','eu-west-1','eu-west-2','eu-west-3','eu-north-1','sa-east-1','us-west-1','us-west-2']


def S3_Bucket_Set_Encryption(accounts,region):
    for acct in accounts:
        session = boto3.Session(profile_name=acct)
        for location in region:
            s3 = session.client('s3',region_name=location)
            ListBucket_Response = s3.list_buckets()
            for bucket in (ListBucket_Response['Buckets']):

                try:
                    Bucket_Encryption_Status_Response = s3.get_bucket_encryption(Bucket=bucket['Name'])

                except:

                    Bucket_Encrypting_Response = s3.put_bucket_encryption(Bucket=bucket['Name'],ServerSideEncryptionConfiguration={'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}},] })
                    if Bucket_Encrypting_Response['ResponseMetadata']['HTTPStatusCode'] == 200:
                        print(bucket['Name']+" Is now Encrypted!")

                    else:
                        print("Error Occured with the api call!")


S3_Bucket_Set_Encryption(accounts,region)
