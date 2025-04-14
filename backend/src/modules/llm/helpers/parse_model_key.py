def parse_model_key(model_key: str):
    return model_key.split(':') if ':' in model_key else [model_key, model_key]
