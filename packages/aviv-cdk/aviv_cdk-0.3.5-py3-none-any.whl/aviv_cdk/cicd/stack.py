import typing
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ssm,
    aws_iam,
    pipelines
)
from . import (
    sources as gh_sources
)

class CodePipelineStack(Stack):
    __connections: dict={}
    __connections_ssm: dict={}
    __sources: dict={}
    pipeline: pipelines.CodePipeline
    step: pipelines.ShellStep
    source: pipelines.CodePipelineSource

    def __init__(
            self, scope: Construct, construct_id: str, *,
            connections: dict=None,
            self_pipeline: bool=True,
            repository: typing.Union[str, gh_sources.SourceRepositoryAttrs]=None,
            code_build_clone_output: bool=True,
            trigger_on_push: bool=None,
            shellstep: typing.Union[dict, pipelines.ShellStepProps]={},
            codepipeline: typing.Union[dict, pipelines.CodePipelineProps]={},
            **kwargs) -> None:
        """[summary]

        Args:
            scope (Construct): [description]
            construct_id (str): [description]
            connections (dict, optional): A dict keyed by 'owner' of codestar-connections arn (or ssm parameters to them). Defaults to None.
            self_pipeline (bool, optional): Generate a basic CodePipeline + ShellStep. Defaults to True.
            repository (typing.Union[str, gh_sources.SourceRepositoryAttrs], optional): the main Github source repository. Defaults to None.
            code_build_clone_output (bool, optional): Clone github repo. Defaults to True.
            trigger_on_push (bool, optional): [description]. Defaults to None.
            shellstep (typing.Union[dict, pipelines.ShellStepProps], optional): Arguments for ShellStep action. Defaults to {'input': repository, 'commands': [...cdk basic pipeline sample commands...]}.
            codepipeline (typing.Union[dict, pipelines.CodePipelineProps], optional): Arguments for CodePipeline. Defaults to {repository + shellstep}.
        """
        super().__init__(scope, construct_id, **kwargs)

        if connections:
            self.connections = connections

        if self_pipeline:
            if not 'input' in shellstep:
                if not repository:
                    info = gh_sources.git_repository_info()
                    repository = f"{info.get('url')}@{info.get('branch')}"
                shellstep['input'] = self.add_source(repository=repository, code_build_clone_output=code_build_clone_output, trigger_on_push=trigger_on_push)
            self.step = self.shellstep(**shellstep)
            self.pipeline = self.codepipeline(step=self.step, self_pipeline=self_pipeline, **codepipeline)

    def shellstep(self, **shellstep) -> pipelines.ShellStep:
        if not 'commands' in shellstep:
            shellstep['commands'] = [
                "npm install -g aws-cdk",
                "python -m pip install aws-cdk-lib aviv-cdk",
                "cdk synth"
            ]
        return pipelines.ShellStep("Synth", **shellstep)

    def codepipeline(self, step: pipelines.ShellStep, *, self_pipeline: bool=False, **cpattr) -> pipelines.CodePipeline:
        cpipe = pipelines.CodePipeline(
            self, "Pipeline",
            synth=step,
            **cpattr
        )
        if self_pipeline and self.__connections_ssm:
            self.ssm_policies(cpipe)
        return cpipe

    def add_source(self, repository: typing.Union[str, gh_sources.SourceRepositoryAttrs], code_build_clone_output: bool=None, trigger_on_push: bool=None) -> pipelines.CodePipelineSource:
        if isinstance(repository, str):
            repository = gh_sources.git_url_split(repository)
        sname = f"{repository['owner']}/{repository['repo']}"
        self.sources[sname] = pipelines.CodePipelineSource.connection(
            repo_string=sname,
            branch=repository['branch'],
            connection_arn=self.connections[repository['owner']],
            code_build_clone_output=code_build_clone_output,
            trigger_on_push=trigger_on_push
        )
        return self.sources[sname]

    @property
    def sources(self) -> dict:
        return self.__sources

    @sources.setter
    def sources(self, sources: dict) -> None:
        for name, url in sources.items():
            self.__sources[name] = url

    @property
    def connections(self) -> dict:
        return self.__connections

    @connections.setter
    def connections(self, connections: dict) -> None:
        for cname, connection_arn in connections.items():
            if connection_arn.startswith('aws:ssm:'):
                self.__connections_ssm[cname] = connection_arn.replace('aws:ssm:', '')
                connection_arn = aws_ssm.StringParameter.value_from_lookup(
                    self, parameter_name=connection_arn.replace('aws:ssm:', '')
                )
            self.__connections[cname] = connection_arn

    def ssm_policies(self, pipeline: pipelines.CodePipeline):
        """Add required IAM policy to codebuild project role in order to fetch SSM Parameters
        (used to store codestar-connections arn per Github 'owner' (aka Github organization))

        Args:
            pipeline (pipelines.CodePipeline): [description]
        """
        pipeline.build_pipeline()
        pipeline.synth_project.add_to_role_policy(aws_iam.PolicyStatement(
            actions=["ssm:GetParameter"],
            resources=list(f"arn:aws:ssm:{self.region}:{self.account}:parameter{connect_ssm}" for connect_ssm in self.__connections_ssm.values()),
            effect=aws_iam.Effect.ALLOW
        ))
