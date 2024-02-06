from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_efs as efs
from constructs import Construct
from aws_cdk import RemovalPolicy

class EfsConstruct(Construct):
    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, efs_sg: ec2.SecurityGroup, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create the EFS filesystem using the existing security group and automatically create mount targets
        self.efs_file_system = efs.FileSystem(
            self, "EfsFileSystem",
            vpc=vpc,
            security_group=efs_sg,  # Use the existing EFS security group
            encrypted=True,
            lifecycle_policy=efs.LifecyclePolicy.AFTER_7_DAYS,  # Optional: Transition to Infrequent Access after 7 days
            performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,
            throughput_mode=efs.ThroughputMode.BURSTING,
            removal_policy=RemovalPolicy.DESTROY,  # Caution: Adjust according to your deployment strategy
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)  # Specify the subnet selection if needed
        )

