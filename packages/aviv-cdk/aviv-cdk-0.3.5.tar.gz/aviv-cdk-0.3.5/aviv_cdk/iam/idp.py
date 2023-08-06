import requests
from constructs import Construct
from aws_cdk import CfnOutput
from aws_cdk import (
    aws_iam,
    aws_ssm
)


class SamlProvider(aws_iam.SamlProvider):
    ssm_parameter_name: str=''
    def __init__(
            self,
            scope: Construct,
            id: str,
            name: str,
            saml_metadata_url: str=None,
            saml_metadata_document: str=None,
            ssm_parameter_name: str=None
            ) -> None:
        """Create an IAM SAML Identity Provider

        Args:
            scope (Construct): [description]
            id (str): [description]
            name (str): IAM idp Name
            idp_url (str, optional): [description]. Defaults to None.
            saml_metadata_document (str, optional): [description]. Defaults to None.
        """

        # Load SSO SAML metadata
        if saml_metadata_url:
            resp = requests.get(url=saml_metadata_url)
            saml_metadata_document = resp.text
        if not saml_metadata_document:
            raise AttributeError("Need saml_metadata_url or saml_metadata_document")

        super().__init__(
            scope, id,
            name=name,
            metadata_document=aws_iam.SamlMetadataDocument.from_xml(saml_metadata_document)
        )
        self.ssm_parameter_name = ssm_parameter_name
        CfnOutput(self.stack, f"{self.node.id}-arn", value=self.saml_provider_arn)
        if self.ssm_parameter_name:
            aws_ssm.StringParameter(self.stack, f"{self.node.id}-ssm", string_value=self.saml_provider_arn, parameter_name=self.ssm_parameter_name)
            CfnOutput(self.stack, f"{self.node.id}-ssm-name", value=self.ssm_parameter_name)


def SamlFederatedPrincipal(federated: str) -> aws_iam.FederatedPrincipal:
    return aws_iam.FederatedPrincipal(
        federated=federated,
        conditions={
            'StringEquals': {'SAML:aud': 'https://signin.aws.amazon.com/saml'}
        },
        assume_role_action='sts:AssumeRoleWithSAML'
    )
