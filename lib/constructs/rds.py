from aws_cdk import aws_rds as rds, aws_ec2 as ec2, aws_kms as kms, RemovalPolicy
from aws_cdk import aws_secretsmanager as secretsmanager
from constructs import Construct

class RdsMysqlConstruct(Construct):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, db_security_group: ec2.SecurityGroup, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Fetch the existing secret by its ARN
        db_secret = secretsmanager.Secret.from_secret_complete_arn(
            self, 
            "DbSecret", 
            "arn:aws:secretsmanager:eu-west-3:943240599753:secret:/rds/mysql/credentials-tg3CzL"
        )

        # RDS MySQL database instance
        self.db_instance = rds.DatabaseInstance(
            self, "MyRdsInstance",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO  # Suitable for Free Tier
            ),
            vpc=vpc,
            vpc_subnets={
                "subnet_type": ec2.SubnetType.PRIVATE_ISOLATED
            },
            security_groups=[db_security_group],
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,
            credentials=rds.Credentials.from_secret(db_secret),  # Use the existing secret for credentials
            allocated_storage=20  # Specified to comply with Free Tier where applicable
        )
