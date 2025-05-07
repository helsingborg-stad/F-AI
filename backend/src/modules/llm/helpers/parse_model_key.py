from typing import Tuple


def parse_model_key(model_key: str) -> Tuple[str, str]:
    if ':' in model_key:
        split = model_key.split(':')
        return split[0], split[1]
    return model_key, model_key
