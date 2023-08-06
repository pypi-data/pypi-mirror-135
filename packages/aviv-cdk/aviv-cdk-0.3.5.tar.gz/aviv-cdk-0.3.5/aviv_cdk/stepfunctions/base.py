from aws_cdk import (
    aws_lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    core
)


class Stepfunctions(core.Construct):
    statemachine: sfn.IStateMachine = None
    start: sfn.IChainable = None

    def __init__(self, scope: core.Construct, id: str, *, start: sfn.IChainable=None) -> None:
        super().__init__(scope, id)

        if not start:
            start = sfn.Pass(self, 'Pass')
        self.start = start

    def machine(self, name: str='stateMachine', timeout: int=1) -> sfn.StateMachine:
        self.statemachine = sfn.StateMachine(
            self, name,
            definition=self.start,
            timeout=core.Duration.minutes(timeout)
        )
        return self.statemachine

    def _wait(self, path:str="$.wait_time") -> sfn.Wait:
        return sfn.Wait(
            self, 'waiter',
            time=sfn.WaitTime.seconds_path(path=path)
        )

    def _invoke_lambda(self, name: str, fx: aws_lambda.IFunction=None,
        code: aws_lambda.AssetCode=None, handler: str=None, runtime=aws_lambda.Runtime.PYTHON_3_7,
        **invoke_attr) -> sfn_tasks.LambdaInvoke:
        if not fx:
            fx = aws_lambda.Function(
                self, "fxi_{}".format(name),
                code=code,
                handler=handler,
                runtime=runtime
            )
        return sfn_tasks.LambdaInvoke(
            self, "{}".format(name),
            lambda_function=fx,
            **invoke_attr
        )
