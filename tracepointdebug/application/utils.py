import os


def get_from_environment_variables(config_name, default, type):
    env_variables = os.environ

    for var_name in env_variables:
        if var_name.upper() == config_name:
            return type(env_variables.get(var_name).strip())
    return default
