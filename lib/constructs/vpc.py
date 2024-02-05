# vpc.py
import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from constructs import Construct


class CustomVPC(Construct):
    def __init__(self, scope: Construct, id:str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        self.vpc = ec2.Vpc(self, "MyCustomVPC",
                           max_azs=3,
                           cidr="10.0.0.0/16",
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name="PublicSubnet",
                                   subnet_type=ec2.SubnetType.PUBLIC,
                                   cidr_mask=24
                               ),
                               ec2.SubnetConfiguration(
                                   name="PrivateSubnet",
                                   subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                                   cidr_mask=24
                               ),
                               ec2.SubnetConfiguration(
                                   name="IsolatedSubnet",
                                   subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                                   cidr_mask=24
                               )
                           ],
                           enable_dns_hostnames=True,
                           enable_dns_support=True)
        # Define NAT Gateways for each Public Subnet if required
        # AWS CDK automatically creates NAT Gateways for PRIVATE_WITH_NAT subnets
        # in the Public Subnets and associates them with private subnets.

        # Output the VPC ID and subnet IDs as attributes of the construct for easy access
        self.vpc_id = self.vpc.vpc_id
        self.public_subnets = [subnet.subnet_id for subnet in self.vpc.public_subnets]
        self.private_subnets = [subnet.subnet_id for subnet in self.vpc.private_subnets]
        self.isolated_subnets = [subnet.subnet_id for subnet in self.vpc.isolated_subnets]