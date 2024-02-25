import json
import os
from typing import TypeVar



def load_env_val(key: str, default=None, allow_none=False):
    var = os.environ.get(key, default=default)
    failure_message = (
        f"Failed to load env var with key:{key}, default:{default}, allow_none:{allow_none}"
    )
    if var is not None and isinstance(var, str):
        if var.startswith("_json_"):
            try:
                var = json.loads(var[6:])
            except json.JSONDecodeError:
                raise RuntimeError(failure_message)
    elif var is None and not allow_none:
        raise RuntimeError(failure_message)
    return var
