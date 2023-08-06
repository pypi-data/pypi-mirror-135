import constructs
import typing
from aws_cdk import (
    aws_secretsmanager,
    aws_rds,
    core
)


class Aurora(core.Construct):
    def __init__(
        self,
        scope: typing.Optional[constructs.Construct]=None,
        id: typing.Optional[str]=None,
        engine_version: aws_rds.EngineVersion=None,
        database_type: typing.Literal['mysql', 'postgresql']='mysql',
        database_name: str='database',
        master_username: str='admin',
        master_password: aws_secretsmanager.CfnSecret=None
        ) -> None:

        super().__init__(scope=scope, id=id)

        if not engine_version:
            if database_type == 'mysql':
                engine_version = aws_rds.AuroraMysqlEngineVersion.aurora_mysql_major_version
            elif database_type == 'mysql':
                engine_version = aws_rds.AuroraPostgresEngineVersion.aurora_postgres_major_version

        master_user_password = master_password.secret_value.to_string()

        aws_rds.CfnDBCluster(
            self,
            id='rds',
            engine='aurora-{}'.format(database_type),
            engine_mode='serverless',
            engine_version=engine_version,
            backup_retention_period=15,
            storage_encrypted=True,
            # Database info
            database_name=database_name,
            master_username=master_username,
            master_user_password=master_user_password,

        )