import aws_cdk as cdk
from aws_cdk import Stack, App
from constructs import Construct
from lib.constructs.vpc import CustomVPC
from lib.constructs.sg import WordpressSecurityGroups


class WordpressAwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Instantiate the CustomVPC construct
        custom_vpc = CustomVPC(self, "MyCustomVPC")

        # Instantiate the WordPressSecurityGroups construct
        wp_sg = WordpressSecurityGroups(self, "WordPressSecurityGroups", vpc=custom_vpc.vpc)



# app = App()
# WordpressAwsStack(app, "WordpressAwsStack")
# app.synth()
