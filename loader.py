import tomllib

def load_config(dateipfad="config/settings.toml"):
    with open(dateipfad, "rb") as datei:
        konfig = tomllib.load(datei)
    return konfig
