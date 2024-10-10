import boto3

# Create a Boto3 client for EC2 and AutoScaling
ec2_client = boto3.client("ec2")
autoscaling_client = boto3.client("autoscaling")

# Create a launch configuration
launch_config_name = "my_launch_configuration"
image_id = "ami-12345abcde"  # Example AMI ID
instance_type = "t2.micro"
launch_configuration = autoscaling_client.create_launch_configuration(
    LanuchConfigurationName=launch_config_name,
    ImageID=image_id,
    InstanceType=instance_type,
)

# Create auto-scaling group
auto_scaling_group_name = "my_auto_scaling_group"
subnet_ids = "subnet-67890"  # Example subnet ID
auto_scaling_group = autoscaling_client.create_autoscaling_group(
    AutoScalingGroupName=auto_scaling_group_name,
    LaunchConfiguration=launch_config_name,
    MinSize=1,
    MaxSize=5,
    VPCZoneIdentifier=subnet_ids,
)

# Define scaling policies
scale_up_policy = autoscaling_client.put_scaling_policy(
    AutoScalingGroupName=auto_scaling_group_name,
    PolicyName="scale_up",
    ScalingAdjustment=1,
    AdjustmentType="ChangeInCapacity",
    Cooldown=300,
    MetricAggregationType="Average",
)

scale_down_policy = autoscaling_client.put_scaling_policy(
    PolicyName="scale_down",
    ScalingAdjustment=1,
    AdjustmentType="ChangeInCapacity",
    Cooldown=300,
    MetricAggregationType="Average",
)

# Print out the policy ARNs
print("Scale Up Policy ARN:", scale_up_policy["PolicyARN"])
print("Scale Down Policy ARN:", scale_down_policy["PolicyARN"])
