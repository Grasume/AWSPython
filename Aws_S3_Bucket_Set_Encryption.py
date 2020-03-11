import boto3

accounts = []
region = []


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
