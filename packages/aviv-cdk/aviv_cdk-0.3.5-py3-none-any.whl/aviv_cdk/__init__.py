__version__='0.3.5'

def json_load_configs(path: str):
    import os
    configs = dict()
    filter_json = lambda x: x.endswith('.json')
    for (dirpath, dirs, files) in os.walk('{}'.format(path)):
        for filename in filter(filter_json, files):
            filepath = f"{dirpath}/{filename}"
            configs[f"{filepath}"] = json_load(filepath)
    return configs

def json_load(filename: str) -> dict:
    import json
    with open(filename) as cfgfile:
        return json.load(cfgfile)

def load_yaml(filename: str) -> object:
    import yaml
    with open(filename, encoding="utf8") as fp:
        with fp.read() as bsfile:
            return yaml.safe_load(bsfile)
