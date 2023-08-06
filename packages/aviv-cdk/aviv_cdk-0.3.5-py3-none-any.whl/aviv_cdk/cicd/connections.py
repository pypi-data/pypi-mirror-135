from constructs import Construct
from aws_cdk import (
    aws_codestarconnections,
    aws_ssm,
    CfnOutput
)


class GithubConnection(Construct):
    connection = aws_codestarconnections.CfnConnection

    def __init__(self, scope: Construct, id: str, connection_name: str, *, host_arn: str=None, ssm_parameter_space: str='/github/connections', **connection_args) -> None:
        super().__init__(scope, id)
        if host_arn:
            connection_args['host_arn'] = host_arn
        self.connection = aws_codestarconnections.CfnConnection(
            self, 'github-connection',
            connection_name=connection_name,
            provider_type='GitHub',
            **connection_args
        )
        CfnOutput(
            self, "output",
            value=self.connection.attr_connection_arn,
            description="Validate with Github app connection at: https://console.aws.amazon.com/codesuite/settings/connections"
        )
        if ssm_parameter_space:
            aws_ssm.StringParameter(
                self, "ssm",
                string_value=self.connection.attr_connection_arn,
                parameter_name=f"{ssm_parameter_space}/{connection_name}"
            )
