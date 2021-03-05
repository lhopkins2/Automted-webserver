#!/usr/bin/env python3
import boto3
import sys
import subprocess
import time

ec2 = boto3.resource('ec2', region_name='eu-west-1')
s3 = boto3.resource('s3')

#Create VPC
vpc = ec2.create_vpc(CidrBlock='10.0.0.1/16')
#VPC is named
vpc.wait_until_available()
vpc.create_tags(Tags=[{"Key": "My VPC", "Value": "Default VPC"}])
print('VPC was been created with the ID: ', vpc.id)

#create vpc internet gateway
gateway = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId = gateway.id)
print('Internet gateway is created with ID: ', gateway.id)

#Create the route table
routeTable = vpc.create_route_table()
route = routeTable.create_route(DestinationCidrBlock='0.0.0.0/0',GatewayId=gateway.id)
print('Route table created with ID: ', routeTable.id)

#Create Subnets
subnet = ec2.create_subnet(CidrBlock='10.0.0.1/24', VpcId=vpc.id)
print('Subnet created with ID: ', subnet.id)

#Connect subnet to route table
routeTable.associate_with_subnet(SubnetId=subnet.id)

#Create a security Group
sg = ec2.create_security_group(GroupName= 'HTTPSSHConnect', Description='Open connect', VpcId=vpc.id)
sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort= 22, ToPort= 22)
sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort= 80, ToPort= 80)
print('Security group created under ID: ' , sg.id)

#Instance is created
instances = ec2.create_instances(
    ImageId='ami-096f43ef67d75e998',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.nano',
    KeyName='lhkey1',
    #SecurityGroupIds=['sg-00c278e5cf3ab4e0d'])
    NetworkInterfaces = [{'SubnetId' : subnet.id, 'DeviceIndex': 0, 'AssociatePublicIpAddress': True, 'Groups': [sg.id]}])

#Tags are set and program waits until instance is running
instanceId = instances[0].id
print ('Starting...')
ec2.Instance(instanceId).wait_until_running()
print ('Instance created and running with the ID: ', instanceId)
nameTag = {'Key' : 'Test', 'Value' : 'Demo Instance'}
instances[0].create_tags(Tags=[nameTag])
ip = instances[0].public_ip_address
ipStr = str(ip)

#User data script is imported
print("User data script is running...")
try:
    time.sleep(30)
    importUserData = 'scp -o StrictHostKeyChecking=no -i lhkey1.pem userdata.sh ec2-user@'+ipStr + ":."
    print (importUserData)
    responseImportUserData = subprocess.run(importUserData, shell=True)
    
except :
    print('Script failed, try again? (y/n)')
    input1 = input()
    if input1 == 'y' or input1 == 'Y' :
        importUserData = 'scp -o StrictHostKeyChecking=no -i lhkey1.pem userdata.sh ec2-user@'+ipStr + " ':.' "
        print (importUserData)
        responseImportUserData = subprocess.run(importUserData, shell=True)

#run user script
authUserData = 'ssh -i lhkey1.pem ec2-user@' + ipStr + " 'chmod 700 userdata.sh' "
print(authUserData)
responseAuthUserData = subprocess.run(authUserData, shell=True)
runUserData = 'ssh -i lhkey1.pem ec2-user@'+ ipStr + " ' sudo ./userdata.sh' "
print(runUserData)
responseRunUserData = subprocess.run(runUserData, shell=True)
print('Web server now running')

#Import and run monitoring script
try: 
    importMonitor = 'scp -o StrictHostKeyChecking=no -i lhkey1.pem monitor.sh ec2-user@'+ipStr + ":."
    print(importMonitor)
    responseImportMonitor = subprocess.run(importMonitor, shell=True)
    authMonitor = 'ssh -i lhkey1.pem ec2-user@' + ipStr + " 'chmod 700 monitor.sh' "
    print(authMonitor)
    responseAuthMonitor = subprocess.run(authMonitor, shell=True)
    runMonitor = 'ssh -i lhkey1.pem ec2-user@'+ ipStr + " ' sudo ./monitor.sh' "
    print(runMonitor)
    responseRunMonitor = subprocess.run(runMonitor, shell=True)
    print('Monitor is running...')
except Exception as e:
    print(e)


#Create s3 bucket
try:
    response = s3.create_bucket(Bucket='lhopkinsbucket2021', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    print (response)
except Exception as e:
    print(e)

#import image to bucket
importImage = "curl https://witacsresources.s3-eu-west-1.amazonaws.com/image.jpg >> image.jpg"
print (importImage) 
responseImportImage = subprocess.run(importImage, shell=True)
try:
    response1 = s3.Object('lhopkinsbucket2021', 'image.jpg').put(Body=open('image.jpg', 'rb'))
    object = s3.Bucket('lhopkinsbucket2021').Object('image.jpg')
    object.Acl().put(ACL ='public-read')
    print (response1)
except Exception as e:
    print (e)


#run web server script 
try:
    importConf = 'scp -o StrictHostKeyChecking=no -i lhkey1.pem configure.sh ec2-user@'+ipStr + ":."
    print(importConf)
    responseImportConf = subprocess.run(importConf, shell=True)
    authConf = 'ssh -i lhkey1.pem ec2-user@' + ipStr + " 'chmod 700 configure.sh' "
    print(authConf)
    responseAuthConf = subprocess.run(authConf, shell=True)
    runConf = 'ssh -i lhkey1.pem ec2-user@'+ ipStr + " ' sudo ./configure.sh' "
    print(runConf)
    responseRunConf = subprocess.run(runConf, shell=True)
    print('Configure web page is running...')
except Exception as e:
    print(e)

print('Instance running inside of a VPC in a public subnet with the info: \nPublic IP: ' + ipStr + '\nInstance ID: '  \
    + instanceId + '\nVPC ID: ' + vpc.id + '\nSubnet ID: ', subnet.id)













