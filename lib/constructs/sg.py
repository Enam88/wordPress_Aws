

#sg.py
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

        # Web Security Group
        self.web_sg = ec2.SecurityGroup(
            self, "WebSecurityGroup",
            vpc=vpc,
            description="Security group for web instances",
            allow_all_outbound=True
        )
        # Allow web traffic from the internet on standard HTTP and HTTPS ports
        # These rules are for traffic coming through the ALB to the web servers
        self.web_sg.add_ingress_rule(
            peer=self.bastion_sg,
            connection=ec2.Port.tcp(22),
            description="SSH access from Bastion"
        )

        # Public ALB Security Group
        self.public_alb_sg = ec2.SecurityGroup(
            self, "PublicAlbSecurityGroup",
            vpc=vpc,
            description="Security group for the public Application Load Balancer",
            allow_all_outbound=True
        )
        # Allow HTTP and HTTPS traffic from anywhere
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

        # Attach the ALB security group to the web security group rules after it's defined
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

        # Database Security Group
        self.db_sg = ec2.SecurityGroup(
            self, "DatabaseSecurityGroup",
            vpc=vpc,
            description="Security group for RDS instances",
            allow_all_outbound=True
        )
        # Allow MySQL traffic from the web servers
        self.db_sg.add_ingress_rule(
            peer=self.web_sg,
            connection=ec2.Port.tcp(3306),
            description="MySQL access from Web"
        )

        # ElastiCache Security Group
        self.elasticache_sg = ec2.SecurityGroup(
            self, "ElastiCacheSecurityGroup",
            vpc=vpc,
            description="Security group for ElastiCache instances",
            allow_all_outbound=True
        )
        # Allow Memcached traffic from the web servers
        self.elasticache_sg.add_ingress_rule(
            peer=self.web_sg,
            connection=ec2.Port.tcp(11211),
            description="Memcached access from Web"
        )

        # EFS Security Group
        self.efs_sg = ec2.SecurityGroup(
            self, "EfsSecurityGroup",
            vpc=vpc,
            description="Security group for EFS",
            allow_all_outbound=True
        )
        # Allow NFS traffic from the web servers and bastion host
        self.efs_sg.add_ingress_rule(
            peer=self.web_sg,
            connection=ec2.Port.tcp(2049),
            description="NFS access from Web"
        )
        self.efs_sg.add_ingress_rule(
            peer=self.bastion_sg,
            connection=ec2.Port.tcp(2049),
            description="NFS access from Bastion"
        )