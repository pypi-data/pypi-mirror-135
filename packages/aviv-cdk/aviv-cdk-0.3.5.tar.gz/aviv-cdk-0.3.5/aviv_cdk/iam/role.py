import typing
from constructs import Construct
from aws_cdk import (
    Duration,
    aws_iam
)


class Role(aws_iam.Role):
    def __init__(
            self, scope: Construct, id: str, *,
            assumed_by: aws_iam.IPrincipal,
            description: str=None,
            policies: list=None,
            external_ids=None,
            inline_policies=None,
            managed_policies: typing.Sequence[aws_iam.IManagedPolicy]=[],
            aws_managed_policies: typing.Sequence[aws_iam.IManagedPolicy]=[],
            max_session_duration: Duration=None,
            path: str=None,
            permissions_boundary: aws_iam.IManagedPolicy=None,
            role_name: str=None
        ) -> None:
        """Same as a regular CDK AWS IAM Role except the Role name is defined by the CDK object 'id'.

        Args:
            scope (Construct): CDK Contruct/Stack
            id (str): Role id
            assumed_by: The IAM principal which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
            description: A description of the role. It can be up to 1000 characters long. Default: - No description.
            policies: A list of AWS pre-defined IAM policies (lookup in arn:aws:iam::aws:policy/)
            external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
            inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
            managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromManagedPolicyName(policyName))``. Default: - No managed policies.
            aws_managed_policies: A list of AWS managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
            max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
            path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
            permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
            role_name: The IAM role name
        """
        if isinstance(assumed_by, list):
            assumed_by = self._assumed_by(assumed_by)
        if isinstance(inline_policies, dict):
            inline_policies = self._inline_policies(inline_policies)
        policies = self._managed_policies(scope, id, managed_policies, aws_managed_policies)
        super().__init__(
            scope=scope, id=id, assumed_by=assumed_by, description=description, external_ids=external_ids, inline_policies=inline_policies,
            managed_policies=policies, max_session_duration=max_session_duration, path=path, permissions_boundary=permissions_boundary, role_name=role_name
        )

    def _inline_policies(self, inline_policies: dict) -> typing.Mapping[str, aws_iam.PolicyDocument]:
        policies = dict()
        for name, policydoc in inline_policies.items():
            if not isinstance(policydoc, aws_iam.PolicyDocument):
                policydoc = aws_iam.PolicyDocument.from_json(policydoc)
            policies[name] = policydoc
        return policies

    def _managed_policies(self, scope: Construct, id: str, managed_policies: list=[], aws_managed_policies: list=[]) -> typing.Sequence[aws_iam.IManagedPolicy]:
        policies = list()
        policies.extend(list(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(managed_policy_name=mp)
            for mp in aws_managed_policies
        ))
        policies.extend(list(
            aws_iam.ManagedPolicy.from_managed_policy_name(scope, f"{id}-{mp}-policy", managed_policy_name=mp)
            for mp in managed_policies
        ))
        return policies

    def _assumed_by(self, principals: typing.Union[aws_iam.IPrincipal, typing.List[str]]) -> aws_iam.IPrincipal:
        pps = list()
        for principal in principals:
            if isinstance(principal, str):
                if principal.startswith("arn:aws"):
                    pps.append(aws_iam.ArnPrincipal(arn=principal))
                else:
                    pps.append(aws_iam.AccountPrincipal(account_id=principal))
            else:
                pps.append(principal)
        if len(pps) > 1:
            return aws_iam.CompositePrincipal(*pps)
        return pps[0]
