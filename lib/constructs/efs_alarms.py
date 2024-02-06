from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subscriptions
from aws_cdk import aws_efs as efs
from constructs import Construct

class EfsAlarmsConstruct(Construct):
    def __init__(self, scope: Construct, id: str, file_system: efs.IFileSystem, email_address: str):
        super().__init__(scope, id)

        # SNS topic for alarm notifications
        topic = sns.Topic(self, "SNSTopic",
                          display_name=f"EFS Alarms Notification",
                          topic_name=f"{file_system.file_system_id}-alarm-notification")

        # Subscribe the provided email address to the topic
        topic.add_subscription(subscriptions.EmailSubscription(email_address))

        # Define the metric for BurstCreditBalance
        burst_credit_balance_metric = cloudwatch.Metric(
            namespace='AWS/EFS',
            metric_name='BurstCreditBalance',
            dimensions_map={
                'FileSystemId': file_system.file_system_id
            }
        )

        # CloudWatch alarm for EFS BurstCreditBalance - Warning
        cloudwatch.Alarm(self, "EfsBurstCreditBalanceWarning",
                         alarm_name=f"EFS BurstCreditBalance Warning",
                         alarm_description="Warning if the BurstCreditBalance is too low",
                         metric=burst_credit_balance_metric,
                         threshold=180 * 60 * 60,  # Adjust based on your needs
                         evaluation_periods=1,
                         comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD)

        # CloudWatch alarm for EFS BurstCreditBalance - Critical
        cloudwatch.Alarm(self, "EfsBurstCreditBalanceCritical",
                         alarm_name=f"EFS BurstCreditBalance Critical",
                         alarm_description="Critical alarm if the BurstCreditBalance is too low",
                         metric=burst_credit_balance_metric,
                         threshold=60 * 60 * 60,  # Adjust based on your needs
                         evaluation_periods=1,
                         comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD)
