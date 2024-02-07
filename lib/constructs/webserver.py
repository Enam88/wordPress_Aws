from aws_cdk import (
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elbv2,
    aws_efs as efs,
    Duration,
)
from constructs import Construct

class WordPressWebServerConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, web_sg: ec2.SecurityGroup, efs_file_system: efs.FileSystem, alb_target_group: elbv2.ApplicationTargetGroup, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # IAM Role for EC2 instances
        role = iam.Role(self, "WebInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ReadOnlyAccess"),
            ]
        )

        # Define UserData for configuring WordPress environment
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "sudo yum update -y",
            "sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2",
            "sudo yum install -y httpd mariadb-server",
            f"sudo mount -t efs -o tls {efs_file_system.file_system_id}:/ /var/www/html",
            "sudo systemctl enable httpd",
            "sudo systemctl start httpd",
            # Additional setup commands can be added here.
        )

        # Auto Scaling Group for WordPress web servers
        asg = autoscaling.AutoScalingGroup(self, "WordPressASG",
            vpc=vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            user_data=user_data,
            security_group=web_sg,
            desired_capacity=2,
            min_capacity=1,
            max_capacity=4,
            role=role,
        )

        # Consider restricting SSH access to known IPs for enhanced security
        asg.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "SSH Access")

        # CPU-based Auto Scaling
        asg.scale_on_cpu_utilization("CPUScaling",
            target_utilization_percent=70,
            cooldown=Duration.minutes(5),
        )

        # Attach ASG to ALB Target Group
        asg.attach_to_application_target_group(alb_target_group)
