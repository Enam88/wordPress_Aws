#Wordpress_aws_stack.py
import aws_cdk as cdk
from aws_cdk import Stack, App
from constructs import Construct
from lib.constructs.vpc import CustomVPC
from lib.constructs.sg import WordpressSecurityGroups
from lib.constructs.bastion import BastionHostConstruct
from lib.constructs.efs_construct import EfsConstruct




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





# app = App()
# WordpressAwsStack(app, "WordpressAwsStack")
# app.synth()
