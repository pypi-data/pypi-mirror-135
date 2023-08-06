import typing
from constructs import Construct
from aws_cdk import (
    Duration,
    aws_secretsmanager,
    aws_ssm,
    aws_ec2,
    aws_rds
)



class AvivAuroraCluster(Construct):
    security_group: aws_ec2.SecurityGroup
    vpc: aws_ec2.IVpc
    rds: aws_rds.ServerlessCluster
    secret: aws_secretsmanager.Secret

    def __init__(
            self,
            scope: Construct,
            id: str, *,
            vpc: aws_ec2.IVpc,
            subnets: typing.List[aws_ec2.ISubnet],
            default_database_name: str,
            cluster_identifier: str,
            scaling: aws_rds.ServerlessScalingOptions=None,
            backup_retention: Duration=Duration.days(7),
            deletion_protection: bool=False
            ) -> None:
        super().__init__(scope, id)
        self.vpc = vpc
        self.security_group = self.setup_security_group(
            security_group_name=f"{id}-{cluster_identifier}",
            egress_rules=[dict(
                peer=aws_ec2.Peer.ipv4('127.0.0.1/32'),
                connection=aws_ec2.Port.all_traffic(),
                description="Block all outbound traffic"
            )]
        )

        self.rds = aws_rds.ServerlessCluster(
            self, "cluster",
            engine=aws_rds.DatabaseClusterEngine.AURORA_POSTGRESQL,
            backup_retention=backup_retention,
            cluster_identifier=cluster_identifier,
            default_database_name=default_database_name,
            deletion_protection=deletion_protection,
            parameter_group=aws_rds.ParameterGroup(
                self, "param-group",
                description="Parameter group for Aurora Postgres",
                engine=aws_rds.DatabaseClusterEngine.aurora_postgres(
                    version=aws_rds.AuroraPostgresEngineVersion.VER_10_7
                ),
                parameters={"client_encoding": 'UTF8'}
            ),
            scaling=scaling,
            security_groups=[self.security_group],
            vpc=self.vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnets=subnets)
        )
        self.secret = self.rds.secret

    def rotate_secret(self) -> None:
        """Enable RDS DB secret rotation.
        Make sure your applications are also able to get the new password once refreshed
        """
        hosted_rotation = aws_secretsmanager.HostedRotation.postgre_sql_single_user(
            function_name=f"{self.rds.cluster_identifier}-rotate-secret",
            vpc=self.vpc
        )
        self.rds.secret.deny_account_root_delete()
        self.rds.secret.add_rotation_schedule(
            'rotate',
            automatically_after=Duration.days(42),
            hosted_rotation=hosted_rotation
        )
        self.rds.connections.allow_default_port_from(hosted_rotation)

    def setup_security_group(self, security_group_name:str, allow_all_outbound: bool=False, ingress_rules: list=[], egress_rules: list=[]) -> aws_ec2.SecurityGroup:
        security_group = aws_ec2.SecurityGroup(
            self, 'security-group',
            vpc=self.vpc,
            allow_all_outbound=allow_all_outbound,
            security_group_name=security_group_name,
            description=f"Security Group for DBCluster"
        )
        for ingress_rule in ingress_rules:
            security_group.add_ingress_rule(**ingress_rule)
        for egress_rule in egress_rules:
            security_group.add_egress_rule(**egress_rule)

        return security_group
