from constructs import Construct
from aws_cdk import (
    SecretValue,
    aws_secretsmanager,
    aws_iam
)
from aviv_cdk import secretsmanager


class SecurityCredentials(Construct):
    user: aws_iam.IUser

    def __init__(self, scope: Construct, id: str, user: aws_iam.IUser=None) -> None:
        super().__init__(scope, id)
        self.user = user

    def console_password(self, template: str = None, key: str = None) -> SecretValue:
        secgen = secretsmanager.SecretGenerator(
            self, 'console-password',
            secret_name=f"iam/user/{self.user.user_name}/password",
            template=template,
            key=key
        )
        return secgen.to_string()
 
    def access_key(self):
        self.accesskey = aws_iam.CfnAccessKey(self, 'key', user_name=self.user.user_name)
        aws_secretsmanager.CfnSecret(
            self, 'access-key',
            name=f"iam/user/{self.user.user_name}/accesskey",
            secret_string=f"{{\"AccessKeyId\": \"{self.accesskey.ref}\", "\
                f"\"SecretAccessKey\": \"{self.accesskey.attr_secret_access_key}\"}}"
        )
        return self.accesskey.attr_secret_access_key
