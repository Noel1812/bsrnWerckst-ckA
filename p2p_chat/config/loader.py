import tomllib


# Einlesen der Config-Datei ohne eigene Funktion
# Wenn mehrere Konfigurationsdateien verwendet werden,
# muss der gleiche Code mehrfach geschrieben werden.

#with open("config/settings.toml", "rb") as f:
 #config = tomllib.load(f)
#print(config)

# Funktion zum Laden der Konfiguration aus einer TOML-Datei
# genau dafür ist die Funktion gedacht, damit der Code nicht mehrfach geschrieben werden muss.
def load_config(dateipfad="config/settings.toml"):
    with open(dateipfad, "rb") as datei:
        konfig = tomllib.load(datei)
    return konfig

