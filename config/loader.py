import tomllib  # Modul zum Einlesen von TOML-Dateien (ab Python 3.11)

##
# @file loader.py
# @brief Lädt Konfigurationsdaten aus einer TOML-Datei in ein Dictionary.
#
# Diese Funktion habe ich geschrieben, damit ich die Konfiguration zentral
# einlesen kann und nicht an mehreren Stellen im Projekt den gleichen Code
# kopieren muss. In Java hätte ich vermutlich eine eigene Klasse für sowas gemacht
# mit einer static Methode oder so, hier geht's einfach mit einer Funktion.
#
# Das ist sauberer, übersichtlicher und wenn sich der Pfad oder das Format mal
# ändern sollte, muss ich nur an einer Stelle etwas anpassen.
#
# @param dateipfad Pfad zur TOML-Datei (Standard: "config/settings.toml")
# @return Dictionary mit den geladenen Werten
# @throws FileNotFoundError wenn die Datei nicht existiert
# @throws tomllib.TOMLDecodeError bei ungültigem TOML-Inhalt
# @note Funktioniert erst ab Python 3.11, da `tomllib` vorher nicht dabei war.
#
def load_config(dateipfad="config/settings.toml"):
    with open(dateipfad, "rb") as datei:
        konfig = tomllib.load(datei)
    return konfig

