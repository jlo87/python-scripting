import boto3

# Create a Boto3 client for EC2 and AutoScaling
ec2_client = boto3.client('ec2')
autoscaling_client = boto3.client('autoscaling')

# Create a launch configuration
launch_config_name = "my_launch_configuration"
image_id = "ami-12345abcde" # Example AMI ID
instance_type = "t2.micro"
launch_configuration = autoscaling_client.create_launch_configuration(
    LanuchConfigurationName=launch_config_name,
    ImageID=image_id,
    InstanceType=instance_type
)

# Create auto-scaling group
auto_scaling_group_name = "my_auto_scaling_group"