#Wordpress_aws_stack.py
import aws_cdk as cdk
from aws_cdk import Stack, App
from constructs import Construct
from lib.constructs.vpc import CustomVPC
from lib.constructs.sg import WordpressSecurityGroups
from lib.constructs.bastion import BastionHostConstruct
from lib.constructs.efs_construct import EfsConstruct
from lib.constructs.efs_alarms import EfsAlarmsConstruct
from lib.constructs.elasticache import ElastiCacheConstruct
from lib.constructs.alb import ALBConstruct  # Make sure to import ALBConstruct
from lib.constructs.rds import RdsMysqlConstruct







class WordpressAwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Instantiate the CustomVPC construct
        custom_vpc = CustomVPC(self, "MyCustomVPC")

        # Instantiate the WordPressSecurityGroups construct
        wordpress_sg = WordpressSecurityGroups(self, "WordPressSecurityGroups", vpc=custom_vpc.vpc)

        # Use the bastion security group from wordpress_sg construct
        bastion_host = BastionHostConstruct(
            self,
            "BastionHost",
            vpc=custom_vpc.vpc,
            bastion_sg=wordpress_sg.bastion_sg,  # Reference to the security group
            key_name="demo-keypair"
        )

        #Instantiate EFS Construct

        efs_construct = EfsConstruct(self, "MyEfsConstruct", vpc=custom_vpc.vpc, efs_sg=wordpress_sg.efs_sg)


        # Instantiate EfsAlarmsConstruct
        # Replace 'your-email@example.com' with the actual email address you want to use for notifications
        efs_alarms = EfsAlarmsConstruct(self, "MyEfsAlarms",
                                        file_system=efs_construct.efs_file_system,
                                        email_address="your-email@example.com")
        
        # Instantiate ElastiCache Construct with the ElastiCache Security Group
        elasticache_construct = ElastiCacheConstruct(self, "MyElastiCacheConstruct",
            vpc=custom_vpc.vpc, 
            cache_security_group=wordpress_sg.elasticache_sg
        )

        
        # Instantiate ALBConstruct with the VPC and ALB security group
        alb_construct = ALBConstruct(
            self,
            "MyALBConstruct",
            vpc=custom_vpc.vpc,
            public_alb_sg=wordpress_sg.public_alb_sg,
            # ssl_certificate_arn="arn:aws:acm:region:account-id:certificate/certificate-id"  # Optional, provide your SSL certificate ARN here
        )
        # Instantiate RdsMysqlConstruct
        rds_mysql_construct = RdsMysqlConstruct(self, "MyRdsMysqlConstruct", vpc=custom_vpc.vpc, db_security_group=wordpress_sg.db_sg)






# app = App()
# WordpressAwsStack(app, "WordpressAwsStack")
# app.synth()
