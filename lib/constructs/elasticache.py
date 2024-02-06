from aws_cdk import aws_elasticache as elasticache
from aws_cdk import aws_ec2 as ec2
from aws_cdk import Stack
from constructs import Construct

class ElastiCacheConstruct(Construct):

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, cache_security_group: ec2.SecurityGroup):
        super().__init__(scope, id)

        # Use isolated subnets for the ElastiCache cluster
        isolated_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)

        # Create a subnet group for ElastiCache using the isolated subnets
        subnet_group = elasticache.CfnSubnetGroup(self, "ElastiCacheSubnetGroup",
            description="ElastiCache Subnet Group for WordPress",
            subnet_ids=[subnet.subnet_id for subnet in isolated_subnets.subnets]
        )

        # Create the ElastiCache cluster
        cache_cluster = elasticache.CfnCacheCluster(self, "ElastiCacheCluster",
            cache_node_type="cache.t3.micro", # Use a node type eligible for the AWS free tier
            cache_subnet_group_name=subnet_group.ref,
            engine="memcached",
            num_cache_nodes=1, # For free tier eligibility, use a single node else len(isolated_subnets.subnets), # Number of nodes based on subnet selection
            az_mode="single-az", # For a single node, az_mode should be "single-az" else  "cross-az", # For high availability across Availability Zones
            vpc_security_group_ids=[cache_security_group.security_group_id],
            tags=[{
                "key": "Name",
                "value": f"WordPress / {Stack.of(self).stack_name}" # Dynamically get the stack name
            }]
        )

        # Output the cache cluster endpoint address
        self.cache_endpoint_address = cache_cluster.attr_redis_endpoint_address
