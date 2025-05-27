import toml

def load_config(path="config/settings.toml"):
    with open(path, "r") as f:
        config = toml.load(f)
    return config
