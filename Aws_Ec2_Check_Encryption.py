import boto3


accounts = []
region = []

def ebs_check_encryption(accounts, region):
    for acct in accounts:
        session = boto3.Session(profile_name=acct)
        for location in region:
            ec2client = session.client('ec2',region_name=location)

            response = ec2client.describe_instances()
            print ("\n Encryption Information for %s \n"%(acct) +"Region "+ location)
            for ec2 in response['Reservations']:
                for image in ec2['Instances']:

                    ImageTags = image.get('Tags')
                    if ImageTags:
                        for tag in image['Tags']:
                            if tag['Key'] == 'Name':
                             servername = tag['Value']
                    for volume in image['BlockDeviceMappings']:
                        ImageVolume = volume['Ebs'].get('VolumeId')

                        volumeResponse = ec2client.describe_volumes(VolumeIds=[ImageVolume])
                        for volumeStatus in  volumeResponse['Volumes'] :

                            serverencryption = volumeStatus['Encrypted']
                            print(servername +' , '+ ImageVolume +' , ' + str(serverencryption))



ebs_check_encryption(accounts, region)
