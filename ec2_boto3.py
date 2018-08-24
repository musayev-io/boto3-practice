import boto3
import sys

# Setup Connection
ec2 = boto3.resource('ec2')

#####################################
# Print Instance Information
#####################################
for instance in ec2.instances.all():
    print(instance.id, instance.state)


#####################################
# Create an Instance
#####################################
instance = ec2.create_instances(
    ImageId='ami-1e299d7e',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro')

print instance[0].id


#####################################
# Terminate an Instance
#####################################
for instance_id in sys.argv[1:]:
    instance = ec2.Instance(instance_id)
    response = instance.terminate()
    print response
