from aws_cdk import (
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_iam as iam,
    CfnMapping,
    Fn,
)
from constructs import Construct


class BastionHostConstruct(Construct):
    def __init__(self, scope: Construct, id: str, vpc: ec2.IVpc, bastion_sg: ec2.ISecurityGroup,  key_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        key_pair_name = "demo-keypair"


        region_map = CfnMapping(
            self,
            "RegionMap",
            mapping={
                "eu-west-3": {"AMI": "ami-06e7d9bed6ecdc388"},
                # Add other regions as needed
            }
        )


        #IAM Role and Instance Profile for Bastion Host
        bastion_role = iam.Role(
            self,
            "BastionInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM")
            ]
        )

        bastion_instance_profile = iam.CfnInstanceProfile(
            self,
            "BastionInstanceprofile",
            roles=[bastion_role.role_name]
        )

        # Launch Configuration for Bastion Host
        bastion_lc = autoscaling.CfnLaunchConfiguration(
            self,
            "BastionLaunchconfiguration",
            image_id=region_map.find_in_map(Fn.ref("AWS::Region"), "AMI"),
            instance_type="t2.micro",
            security_groups=[bastion_sg.security_group_id],
            key_name=key_pair_name,
            iam_instance_profile=bastion_instance_profile.ref
        )

        # Auto Scaling Group for Bastion Host
        bastion_asg = autoscaling.CfnAutoScalingGroup(
            self,
            "BastionAutoScalingGroup",
            min_size='1',
            max_size='1',
            desired_capacity='1',  # Optionally add this line to explicitly set desired capacity
            launch_configuration_name=bastion_lc.ref,
            vpc_zone_identifier=[subnet.subnet_id for subnet in vpc.public_subnets],
            tags=[autoscaling.CfnAutoScalingGroup.TagPropertyProperty(
                key="Name",
                value="Bastion",
                propagate_at_launch=True
            )]
        )