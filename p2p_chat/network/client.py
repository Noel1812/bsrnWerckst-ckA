import socket
import os
from config.loader import load_config

config = load_config("config/settings1.toml")  
HANDLE = config["handle"]
PORT = config["port"]
WHOISPORT = config["whoisport"]
AUTOREPLY = config["autoreply"]
IMAGEPATH = config["imagepath"]

BUFFER_SIZE = 4096


def send_msg(ip, port):
    nachricht = input("Nachricht eingeben: ").strip()
    if nachricht == "":
        print("[Fehler] Leere Nachricht.")
        return


    text = f"MSG {HANDLE} {nachricht}\n"

    try:
        verbindung = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        verbindung.connect((ip, port))
        verbindung.sendall(text.encode("utf-8"))
        verbindung.close()
        print("[Gesendet] Nachricht wurde gesendet.")
    except Exception as fehler:
        print("[Fehler] Nachricht konnte nicht gesendet werden:", fehler)


def send_image(ip, port):
    pfad = input("Pfad zum Bild eingeben: ").strip()
    if not os.path.exists(pfad):
        print("[Fehler] Datei nicht gefunden.")
        return

    dateigroesse = os.path.getsize(pfad)
    header = f"IMG {HANDLE} {dateigroesse}\n"

    try:
        verbindung = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        verbindung.connect((ip, port))

        verbindung.sendall(header.encode("utf-8"))

        with open(pfad, "rb") as datei:
            daten = datei.read()
            verbindung.sendall(daten)

        verbindung.close()
        print("[Gesendet] Bild wurde gesendet.")
    except Exception as fehler:
        print("[Fehler] Bild konnte nicht gesendet werden:", fehler)
