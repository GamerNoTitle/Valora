import os
import yaml

def ReadConf(variable_name, default_value=None):
    # Try to get the variable from the environment
    env_value = os.environ.get(variable_name)

    if env_value is not None:
        return env_value

    # If not found in environment, try to read from config.yml
    try:
        with open("config.yml", "r") as config_file:
            config_data = yaml.safe_load(config_file)
            return config_data.get(variable_name, default_value)
    except FileNotFoundError:
        return default_value
