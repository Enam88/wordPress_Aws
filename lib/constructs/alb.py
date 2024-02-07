from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_certificatemanager as acm
from constructs import Construct
from aws_cdk import Stack
import aws_cdk as cdk

class ALBConstruct(Construct):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, public_alb_sg: ec2.SecurityGroup, ssl_certificate_arn: str = None):
        super().__init__(scope, id)

        # Create an internet-facing ALB
        self.lb = elbv2.ApplicationLoadBalancer(
            self, "PublicApplicationLoadBalancer",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name=f"my-alb-{id.lower()}",
            security_group=public_alb_sg,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        )

        # Create a target group
        self.target_group = elbv2.ApplicationTargetGroup(
            self, "PublicAlbTargetGroup",
            vpc=vpc,
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            health_check=elbv2.HealthCheck(
                interval=cdk.Duration.seconds(30),
                path="/wp-login.php",
                timeout=cdk.Duration.seconds(5),
                unhealthy_threshold_count=5
            ),
            stickiness_cookie_duration=cdk.Duration.minutes(5)
        )

        # Create an HTTP listener and optionally an HTTPS listener if an SSL certificate ARN is provided
        self.http_listener = self.lb.add_listener("HttpListener", port=80, default_action=elbv2.ListenerAction.forward([self.target_group]))

        if ssl_certificate_arn:
            self.https_listener = self.lb.add_listener("HttpsListener", port=443,
                                                        certificates=[elbv2.ListenerCertificate(ssl_certificate_arn)], 
                                                        default_action=elbv2.ListenerAction.forward([self.target_group]))

