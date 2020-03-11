import boto3

def profile():
    print("Please enter the profile set up for the environment you need to run this script for!")
    inputProfile = input()
    return inputProfile

def server():
    print("Please enter the Server Name!(Not FQDN)")
    inputServer = input()
    return inputServer

def region():
    print("Please enter the region!(example: us-east-1)")
    inputRegion = input()
    return inputRegion

def snapshotDescription():
    print("Please enter a Snapshot name based on the above List!")
    inputDescription = input()
    return inputDescription

def ec2InstanceCall(inputServer,ec2client):
    # Gets Instance ID and Az from Instance input
    responseDescribeInstances = ec2client.describe_instances(Filters=[{'Name': 'tag:Name','Values': [str(inputServer)]}])
    for ec2 in responseDescribeInstances['Reservations']:
        for ec2instance in ec2['Instances']:
            instanceId = ec2instance['InstanceId']
            availabilityZone = ec2instance['Placement']['AvailabilityZone']
    return instanceId, availabilityZone

def snapshotCheck(ec2client):
    # Gets List of Snapshots ISO files
    responseDescribeSnapshots = ec2client.describe_snapshots(OwnerIds=['711940113766'])
    for snapshot in responseDescribeSnapshots['Snapshots']:
        isoSnapshot = snapshot.get('Description')
        if "English" in isoSnapshot:
            print(isoSnapshot)

def snapshotCall(inputDescription,ec2client,instanceId):
        #Ges Snapshot information from aws for the iso input
        responseDescribeSnapshots = ec2client.describe_snapshots(OwnerIds=['711940113766'])
        for snapshot in responseDescribeSnapshots['Snapshots']:
            isoSnapshot = snapshot.get('Description')
            if inputDescription in isoSnapshot:
                snapshotId = snapshot.get('SnapshotId')
                #create the Ec2 voulume
                responseCreateVolume = ec2client.create_volume(AvailabilityZone=availabilityZone,SnapshotId=snapshotId)

                #waits for ec2 volume to be ready
                while (ec2resource.Volume(responseCreateVolume.get('VolumeId')).state) != 'available':
                    pass
                #once ec2 is ready attaches the volume to the insanceid above
                response = ec2client.attach_volume(Device='xvdp',InstanceId=instanceId,VolumeId=responseCreateVolume.get('VolumeId'))
                if response['State'] == 'attaching':
                    print("ISO Volume has been Attached!")
                else:
                    print("Error in the Attachments!")


inputProfile = profile()
print("Entered Profile " + inputProfile)
inputRegion = region()
print("Entered Region " + inputRegion)
inputServer = server()
print("Entered Server " + inputServer)

session = boto3.Session(profile_name=inputProfile)
ec2client = session.client('ec2',region_name=inputRegion)
ec2resource = session.resource('ec2',region_name=inputRegion)

instanceId, availabilityZone = ec2InstanceCall(inputServer,ec2client)
print("Available SnapShots")
snapshotList = snapshotCheck(ec2client)


inputDescription = snapshotDescription()
snapshotCall(inputDescription,ec2client,instanceId)
