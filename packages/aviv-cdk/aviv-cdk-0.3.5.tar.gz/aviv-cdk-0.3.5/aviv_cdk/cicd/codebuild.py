import typing
from aws_cdk import (
    aws_codebuild as cb
)


def buildenv(environment_variables: dict) -> typing.Dict[str, cb.BuildEnvironmentVariable]:
    """Facilitate Codebuild environmemt creation
    Simply pass your dict to be turned a env variabltes
    For values that starts with 'aws:sm:', the prefix will be striped off
     and the Codebuild env variable type wil be set to SECRETS_MANAGER.

    Args:
        environment_variables (dict): key/value store to turn into Codebuild Env

    Returns:
        typing.Dict[cb.BuildEnvironmentVariable]: [description]
    """
    envs = dict()
    for env, value in environment_variables.items():
        if isinstance(value, str) and value.startswith('aws:sm:'):
            envs[env] = cb.BuildEnvironmentVariable(
                value=value.replace('aws:sm:', ''),
                type=cb.BuildEnvironmentVariableType.SECRETS_MANAGER
            )
        else:
            envs[env] = cb.BuildEnvironmentVariable(value=value)
    return envs


def load_buildspec(specfile: str='buildspec.yml') -> cb.BuildSpec:
    """Load a buildspec yaml file

    Args:
        specfile ([type]): [description]

    Returns:
        [type]: [description]
    """
    import yaml
    with open(specfile, encoding="utf8") as fp:
        bsfile = fp.read()
        bs = yaml.safe_load(bsfile)
        return cb.BuildSpec.from_object(value=bs)
