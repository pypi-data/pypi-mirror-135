import os
import typing
from constructs import Construct
from aws_cdk import CfnOutput
from aws_cdk import (
    aws_lambda,
    aws_stepfunctions,
    aws_stepfunctions_tasks,
    aws_events,
    aws_events_targets
)

LAMBDAS_RUNTIME = os.environ.get('LAMBDAS_RUNTIME', aws_lambda.Runtime.PYTHON_3_7)
LAMBDAS_PATH = os.environ.get('LAMBDAS_PATH', './lambdas')


class StateMachine(Construct):
    _sm: aws_stepfunctions.IStateMachine = None
    _smprops: dict = {}
    lambdas: dict = {}
    lambdas_assets: aws_lambda.AssetCode
    lambdas_runtime: aws_lambda.Runtime

    def __init__(self, scope: Construct, id: str, *, lambdas_path=LAMBDAS_PATH, lambdas_runtime=LAMBDAS_RUNTIME, **attr) -> None:
        super().__init__(scope, id, **attr)
        self.lambdas_runtime = lambdas_runtime
        self.lambdas_assets = aws_lambda.AssetCode.from_asset(lambdas_path)

    @property
    def sm(self) -> aws_stepfunctions.StateMachine:
        if not self._sm:
            self.sm = aws_stepfunctions.StateMachine(self, 'sm', **self.smprops)
        return self._sm

    @sm.setter
    def sm(self, value: aws_stepfunctions.StateMachine):
        self._sm = value

    @property
    def smprops(self) -> dict:
        if not self._smprops:
            self._smprops = {'definition': aws_stepfunctions.Pass(self, 'pass')}
        return self._smprops

    @smprops.setter
    def smprops(self, value: typing.Union[aws_stepfunctions.StateMachineProps, dict]):
        if isinstance(value, aws_stepfunctions.StateMachineProps):
            value = value.__dict__['_values']
        self._smprops = value

    def launch(self, statemachine_props: aws_stepfunctions.StateMachineProps=None) -> aws_stepfunctions.StateMachine:
        # Main goal is to call self.sm at least once
        self.smprops = statemachine_props
        CfnOutput(self, 'sm-arn', value=self.sm.state_machine_arn)
        return self.sm

    def lambda_function(self, name: str, fx_attr: typing.Union[aws_lambda.FunctionProps, dict]=None) -> aws_lambda.Function:
        if not fx_attr:
            fx_attr = aws_lambda.FunctionProps(
                code=self.lambdas_assets,
                runtime=self.lambdas_runtime,
                handler=f"{name}.handler"
            )

        elif isinstance(fx_attr, dict):
            if 'runtime' not in fx_attr:
                fx_attr['runtime'] = self.lambdas_runtime
            if 'code' not in fx_attr:
                fx_attr['code'] = self.lambdas_assets
            if 'handler' not in fx_attr:
                fx_attr['handler'] = f"{name}.handler"

        if isinstance(fx_attr, aws_lambda.FunctionProps):
            fx_attr = fx_attr.__dict__['_values']

        return aws_lambda.Function(self, f"{name}-lambda", **fx_attr)

    def lambda_task(
            self,
            name: str,
            fx: aws_lambda.IFunction=None,
            fx_attr: aws_lambda.FunctionProps=None,
            invoke: dict={}) -> aws_stepfunctions_tasks.LambdaInvoke:
        """Create a Lambda function step

        Args:
            name (str): [description]
            fx (aws_lambda.IFunction, optional): [description]. Defaults to None.
            fx_attr (aws_lambda.FunctionProps, optional): [description]. Defaults to None.
            invoke (dict, optional): [description]. Defaults to {}.

        Returns:
            aws_stepfunctions_tasks.LambdaInvoke: [description]
        """
        if not fx:
            fx = self.lambda_function(name, fx_attr=fx_attr)
        # Keep a reference to that lambda Function
        self.lambdas[name] = fx
        return aws_stepfunctions_tasks.LambdaInvoke(
            self,
            name,
            lambda_function=fx,
            **invoke
        )

    def cron(self, name: str, cron: dict, *, input: aws_events.RuleTargetInput=None):
        """Schedule CRON-like events for your statemachine

        Args:
            name (str): [description]
            cron (dict): [description]
            input (aws_events.RuleTargetInput, optional): [description]. Defaults to None.
        """
        rule = aws_events.Rule(self, name, schedule=aws_events.Schedule.cron(**cron))
        target = aws_events_targets.SfnStateMachine(
            self.sm,
            input=input
        )
        rule.add_target(target)
