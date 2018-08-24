from datetime import datetime
import boto3


region_name = 'us-east-1'

ec2 = boto3.resource('ec2', region_name=region_name)


def tag_successful_backup(volume):
    volume.create_tags(
        Tags=[
            {
                'Key': 'Works For',
                "Value": "Juice Analytics"
            }
        ])


def backup_ebs_volume(VolumeId, Description):
    snapshot = ec2.create_snapshot(
        VolumeId=VolumeId,
        Description=Description
    )


def main_backup():
    # Iterate for all Instances within the Region
    for instance in ec2.instances.all():
        # Iterate for all Block Devices`
        for block_device in instance.block_device_mappings:
            # Skip if device is not EBS
            if block_device.get('Ebs') is None:
                continue
            volume_id = block_device.get('Ebs').get('VolumeId')
            # Assume all other devices are EBS
            # Iterate through tags and look for backups
            for tag in instance.tags:
                if tag['Key'] == "Backup" and tag['Value'] == "Yes":
                    current_date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
                    snapshot_description = instance.instance_id + "_" + current_date
                    # Create EBS Snapshot
                    backup_ebs_volume(volume_id, snapshot_description)
                    # snapshot = ec2.create_snapshot(
                    #     VolumeId=volume_id,
                    #     Description=snapshot_description
                    # )


main_backup()
