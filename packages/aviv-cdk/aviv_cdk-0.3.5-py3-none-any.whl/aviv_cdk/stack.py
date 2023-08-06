import typing
from aws_cdk import (
    aws_ssm,
    core
)


class Stack(core.Stack):
    def __init__(self,
            scope: typing.Optional[core.Construct]=None,
            id: typing.Optional[str]=None,
            *,
            StackProps: core.StackProps=None) -> None:

        super().__init__(
            scope,
            id,
            **StackProps
        )
