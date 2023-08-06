import sys
import logging
from constructs import Construct
from aws_cdk import (
    CfnOutput,
    aws_events,
    aws_events_targets,
    aws_lambda,
    aws_ssm
)


class Construct(Construct):
    _layers = dict()

    def __init__(self,  scope: Construct, id: str, *, lambdas: dict=None, layers: dict=None):
        super().__init__(scope, id)
        # Process and save AWS Lambda layers
        for layer_name, layer_attr in layers.items():
            self._layers[layer_name] = self.LayerVersion(layer_name, **layer_attr)
        # Process and save AWS Lambda Functions
        for fx_name, fx_attr in lambdas.items():
            self.Function(fx_name, **fx_attr)

    def Function(self, id: str, *, **attr) -> aws_lambda.Function:
        if 'layers' in attr:
            for layer in attr['layers']:
                if layer in self._layers:
                    layer = self._layers[layer]
        fx = aws_lambda.Function(self, id, **attr)
        CfnOutput(self, f"{id}-cfn", value=fx.function_arn)
        return fx

    def LayerVersion(self, id: str, *, remote_account_grant: bool=False, ssm_param: bool=True, **attr) -> aws_lambda.LayerVersion:
        layv = aws_lambda.LayerVersion(self, id **attr)
        if remote_account_grant:
            layv.add_permission('remote-account-grant', account_id='*')
        if ssm_param:
            aws_ssm.StringParameter(
                self, f"{id}-ssm",
                string_value=layv.layer_version_arn,
                parameter_name=f"/layers/{id.replace('-', '/')}"
            )
        CfnOutput(self, f"{id}-cfn", value=layv.from_layer_version_arn)
        return layv
    
    def cron(self, id: str, cron: aws_events.Schedule, *, targets: list=[], event: dict=None, target_args: dict=None, event_attr: dict=None):
        if event:
            event = aws_events.RuleTargetInput.from_object(event)
        if targets:
            for target in targets:
                target = aws_events_targets.LambdaFunction(target, event=event, **target_args)
        return aws_events.Rule(self, id, schedule=cron, targets=targets, **event_attr)


def inline_code(filepath: str) -> str:
    """Streamline file into a string for a simple AWS Lambda

    Args:
        filepath ([type]): [description]

    Returns:
        [type]: [description]
    """
    with open(filepath, encoding="utf8") as fp:
        code = fp.read()
    if sys.getsizeof(code) > 4096:
        logging.warning(f"Code inline size if > 4096: {sys.getsizeof(code)}")
    return code
