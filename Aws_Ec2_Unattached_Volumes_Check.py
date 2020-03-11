import boto3


accounts = []
region = []
def ebs_unattached_volume_check(accounts, region):
    unencrypted = set()
    for acct in accounts:
        session = boto3.Session(profile_name=acct)
        print(acct)
        for location in region:
            ec2client = session.client('ec2',region_name=location)

            response = ec2client.describe_volumes()
            #Gets all Volumes Unencrypted and adds them to unencrypted list
            for volume in response['Volumes']:
                if volume['Encrypted'] == False :
                    for information in volume['Attachments']:
                        unencrypted.add(information['InstanceId'])

            #Takes unencrypted list gets Instance name and Owner and prints the InstanceId and instance name
            print(location)
            for InstanceId in unencrypted:
                describeInstanceResponse =  ec2client.describe_instances(InstanceIds =[InstanceId])
                for instance in describeInstanceResponse['Reservations']:
                    for ec2 in instance['Instances']:
                        ImageTags = ec2.get('Tags')
                        if ImageTags:
                            for tag in ec2['Tags']:
                                if tag['Key'] == 'Name':
                                    name = tag['Value']
                                if tag['Key'] == 'owner':
                                    owner = tag['Value']

                        print(InstanceId + ' Instance Name ' + name)

            unencrypted.clear()

ebs_unattached_volume_check(accounts, region)
