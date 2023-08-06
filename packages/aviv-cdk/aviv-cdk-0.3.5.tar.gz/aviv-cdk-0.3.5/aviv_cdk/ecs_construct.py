import typing
from constructs import Construct
from aws_cdk import (
    aws_certificatemanager,
    aws_ec2,
    aws_ecs,
    aws_ecs_patterns,
    aws_elasticloadbalancingv2
)



class AvivFargateBase(Construct):
    security_group: aws_ec2.SecurityGroup
    vpc: aws_ec2.IVpc
    subnets: aws_ec2.SubnetSelection
    service: aws_ecs.FargateService
    task: aws_ecs.FargateTaskDefinition

    def __init__(
            self,
            scope: Construct,
            id: str,
            *,
            vpc: aws_ec2.IVpc,
            subnets: typing.Sequence[aws_ec2.ISubnet]=None,
            task_definition: aws_ecs.FargateTaskDefinitionProps={},
            container_definition: aws_ecs.ContainerDefinitionOptions=None) -> None:
        super().__init__(scope, id)
        self.vpc = vpc
        if subnets:
            self.subnets = aws_ec2.SubnetSelection(subnets=subnets, one_per_az=True)
        self.security_group = self.setup_security_group()
        self.task_definition = task_definition
        if container_definition:
            self.task_definition.add_container('container', **container_definition._values)


    @property
    def task_definition(self) -> aws_ecs.FargateTaskDefinition:
        return self.task

    @task_definition.setter
    def task_definition(self, task: aws_ecs.FargateTaskDefinitionProps):
        if 'cpu' not in task:
            task['cpu'] = 2048
        if 'memory_limit_mib' not in task:
            task['memory_limit_mib'] = 4096
        self.task = aws_ecs.FargateTaskDefinition(self, 'task', **task)

    def add_container(self, **container_definition):
        self.task_definition.add_container('container', **container_definition)

    def setup_security_group(self, allow_all_outbound: bool=True, ingress_rules: list=[], egress_rules: list=[]) -> aws_ec2.SecurityGroup:
        security_group = aws_ec2.SecurityGroup(
            self, "security-group",
            vpc=self.vpc,
            allow_all_outbound=allow_all_outbound,
            description="Security Group for Fargate"
        )
        for ingress_rule in ingress_rules:
            security_group.add_ingress_rule(**ingress_rule)
        for egress_rule in egress_rules:
            security_group.add_egress_rule(**egress_rule)
        return security_group

    def setup_cluster(self, cluster_name: str=None):
        return aws_ecs.Cluster(
            self, 'Cluster',
            cluster_name=cluster_name,
            vpc=self.vpc,
            enable_fargate_capacity_providers=True
        )



class AvivFargateService(AvivFargateBase):
    cluster: aws_ecs.ICluster

    def __init__(
            self,
            scope: Construct,
            id: str,
            *,
            vpc: aws_ec2.IVpc,
            subnets: typing.Sequence[aws_ec2.ISubnet],
            cluster: aws_ecs.ICluster=None,
            cluster_name: str=None,
            service_name: str,
            container_definition: aws_ecs.ContainerDefinitionOptions,
            desired_count: int=2,
            **kwargs
            ) -> None:
        super().__init__(scope, id, vpc=vpc, subnets=subnets, container_definition=container_definition)

        if not cluster:
            cluster = self.setup_cluster(cluster_name=cluster_name)
        self.service = aws_ecs.FargateService(
            self, 'fargate',
            platform_version=aws_ecs.FargatePlatformVersion.VERSION1_4,
            security_groups=[self.security_group],
            desired_count=desired_count,
            task_definition=self.task_definition,
            vpc_subnets=self.subnets,
            cluster=cluster,
            enable_ecs_managed_tags=True,
            service_name=service_name,
            **kwargs
        )



class AvivLBFargateService(AvivFargateBase):
    def __init__(
            self,
            scope: Construct,
            id: str,
            *,
            vpc: aws_ec2.IVpc,
            subnets: typing.Sequence[aws_ec2.ISubnet],
            cluster: aws_ecs.ICluster=None,
            cluster_name: str=None,
            service_name: str,
            container_definition: aws_ecs.ContainerDefinitionOptions,
            desired_count: int=2,
            public_load_balancer: bool=True,
            listener_port: int=443,
            protocol: aws_elasticloadbalancingv2.Protocol=aws_elasticloadbalancingv2.Protocol.HTTPS,
            domain_name: str,
            domain_zone: str,
            certificate: aws_certificatemanager.ICertificate=None,
            **kwargs) -> None:
        super().__init__(scope, id, vpc=vpc, subnets=subnets, container_definition=container_definition)

        if not cluster and cluster_name:
            cluster = self.setup_cluster(cluster_name=cluster_name)
        self.albfs = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 'fargate',
            platform_version=aws_ecs.FargatePlatformVersion.VERSION1_4,
            security_groups=[self.security_group],
            desired_count=desired_count,
            task_definition=self.task_definition,
            domain_name=domain_name,
            domain_zone=domain_zone,
            certificate=certificate,
            listener_port=listener_port,
            protocol=protocol,
            public_load_balancer=public_load_balancer,
            task_subnets=self.subnets,
            service_name=service_name,
            cluster=cluster,
            **kwargs
        )
        self.service = self.albfs.service
