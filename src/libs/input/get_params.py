import json

def get_params(params_name:str,config_path = 'config.json') -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[params_name]

