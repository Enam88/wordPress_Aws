# import aws_cdk as cdk
# from aws_cdk import aws_ec2 as ec2
# from constructs import Construct


# class WordpressSecurityGroups(Construct):
#     def __init__(self, scope: Construct, id: str, vpc: ec2.IVpc, **kwargs) -> None:
#         super().__init__(scope, id, **kwargs)


#         #Bastion Security Group
#         self.bastion_sg = ec2.SecurityGroup(
#             self, "BastionSecuityGroup",
#             vpc=vpc,
#             description="Security group for Bastion Instances",
#             allow_all_outbound=True

#         )

#         self.bastion_sg.add_ingress_rule(
#             ec2.Peer.ipv4("0.0.0.0/0"),
#             ec2.Port.tcp(22),
#             "SSH access"
#         )

#         #Database Security Group
#         self.db_sg = ec2.SecurityGroup(
#             self, "DatabaseSecurityGroup",
#             vpc=vpc,
#             description="Security group for Amazon RDS cluster",
#             allow_all_outbound=True
#         )

#         #ElastiCache Security Group
#         self.elasticache_sg = ec2.SecurityGroup(
#             self, "ElastiCacheSecurityGroup",
#             vpc=vpc,
#             description="Security Group for ElastiCache Cluster",
#             allow_all_outbound=True

#         )

#         #EFS Security Group
#         self.efs_sg = ec2.SecurityGroup(
#             self, "EfsSecurityGroup",
#             vpc=vpc,
#             description="Security Group for EFS mount targets",
#             allow_all_outbound=True
#         )
#         # self.efs_sg.add_ingress_rule(
#         #     ec2.Peer.ipv4(self.bastion_sg.security_group_id),
#         #     ec2.Port.tcp(2049),
#         #     "NFS access"
#         # )

#         self.efs_sg.add_ingress_rule(
#             peer=self.bastion_sg,
#             connection=ec2.Port.tcp(2049),
#             description="NFS access"
#             )


#         #Public ALB Security Group
#         self.public_alb_sg = ec2.SecurityGroup(
#             self, "PublicAlbSecurityGroup",
#             vpc=vpc,
#             description="Security group for ALB",
#             allow_all_outbound=True
#         )

#         self.public_alb_sg.add_ingress_rule(
#             ec2.Peer.any_ipv4(),
#             ec2.Port.tcp(80),
#             "HTTP access"
#         )

#         self.public_alb_sg.add_ingress_rule(
#             ec2.Peer.any_ipv4(),
#             ec2.Port.tcp(443),
#             "HTTPS access"
#         )

#         #Web Security Group
#         self.web_sg = ec2.SecurityGroup(
#             self, "WebSecurityGroup",
#             vpc=vpc,
#             description="Security group for web instances",
#             allow_all_outbound=True
#         )

#         self.web_sg.add_ingress_rule(
#             ec2.Peer.ipv4(self.public_alb_sg.security_group_id),
#             ec2.Port.tcp(80),
#             "HTTP access from ALB"
#         )

#         self.web_sg.add_ingress_rule(
#         ec2.Peer.ipv4(self.public_alb_sg.security_group_id),
#         ec2.Port.tcp(443),
#         "HTTPs access from ALB"
#         )

#         self.web_sg.add_ingress_rule(
#         ec2.Peer.ipv4(self.public_alb_sg.security_group_id),
#         ec2.Port.tcp(22),
#         "SSH access from Bastion"
#         )

#         #Allow database and ElastiCache security groups to accept connections from web security group
#         self.db_sg.add_ingress_rule(
#             ec2.Peer.ipv4(self.web_sg.security_group_id),
#             ec2.Port.tcp(3306),
#             "MySQL access from Web"
#         )

#         self.db_sg.add_ingress_rule(
#             ec2.Peer.i(self.web_sg.security_group_id),
#             ec2.Port.tcp(11211),
#             "Memcached access from Web"
#         )

import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class WordpressSecurityGroups(Construct):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Bastion Security Group
        self.bastion_sg = ec2.SecurityGroup(
            self, "BastionSecurityGroup",
            vpc=vpc,
            description="Security group for Bastion Instances",
            allow_all_outbound=True
        )
        self.bastion_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(22),
            description="SSH access"
        )

        # Database Security Group
        self.db_sg = ec2.SecurityGroup(
            self, "DatabaseSecurityGroup",
            vpc=vpc,
            description="Security group for Amazon RDS cluster",
            allow_all_outbound=True
        )

        # ElastiCache Security Group
        self.elasticache_sg = ec2.SecurityGroup(
            self, "ElastiCacheSecurityGroup",
            vpc=vpc,
            description="Security Group for ElastiCache Cluster",
            allow_all_outbound=True
        )

        # EFS Security Group
        self.efs_sg = ec2.SecurityGroup(
            self, "EfsSecurityGroup",
            vpc=vpc,
            description="Security Group for EFS mount targets",
            allow_all_outbound=True
        )
        self.efs_sg.add_ingress_rule(
            peer=self.bastion_sg,
            connection=ec2.Port.tcp(2049),
            description="NFS access"
        )

        # Public ALB Security Group
        self.public_alb_sg = ec2.SecurityGroup(
            self, "PublicAlbSecurityGroup",
            vpc=vpc,
            description="Security group for ALB",
            allow_all_outbound=True
        )
        self.public_alb_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="HTTP access"
        )
        self.public_alb_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443),
            description="HTTPS access"
        )

        # Web Security Group
        self.web_sg = ec2.SecurityGroup(
            self, "WebSecurityGroup",
            vpc=vpc,
            description="Security group for web instances",
            allow_all_outbound=True
        )
        self.web_sg.add_ingress_rule(
            peer=self.public_alb_sg,
            connection=ec2.Port.tcp(80),
            description="HTTP access from ALB"
        )
        self.web_sg.add_ingress_rule(
            peer=self.public_alb_sg,
            connection=ec2.Port.tcp(443),
            description="HTTPS access from ALB"
        )
        self.web_sg.add_ingress_rule(
            peer=self.bastion_sg,
            connection=ec2.Port.tcp(22),
            description="SSH access from Bastion"
        )

        # Allow database and ElastiCache security groups to accept connections from web security group
        self.db_sg.add_ingress_rule(
            peer=self.web_sg,
            connection=ec2.Port.tcp(3306),
            description="MySQL access from Web"
        )
        self.elasticache_sg.add_ingress_rule(
            peer=self.web_sg,
            connection=ec2.Port.tcp(11211),
            description="Memcached access from Web"
        )
