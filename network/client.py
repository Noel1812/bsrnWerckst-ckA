import socket
import os
from config.loader import load_config

config = load_config("config/settings4.toml")
HANDLE = config["handle"]
PORT = config["port"]
WHOISPORT = config["whoisport"]
AUTOREPLY = config["autoreply"]
IMAGEPATH = config["imagepath"]

BUFFER_SIZE = 4096

# Liste an Wörtern, die zensiert werden sollen
BLACKLIST = [
    "arschloch",
    "penner",
    "fuck",
    "idiot",
    "dummkopf",
    "arsch",
    "miststück"
    "arschhh"
    "fuckk"
    # beliebig erweiterbar
]

def zensiere_nachricht(text):
    for wort in BLACKLIST:
        maskiert = "*" * len(wort)
        text = text.replace(wort, maskiert).replace(wort.capitalize(), maskiert)
    return text

def create_socket_for_ip(ip):
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return socket.socket(socket.AF_INET6, socket.SOCK_STREAM), True
    except OSError:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM), False

def send_msg(ip, port):
    nachricht = input("Nachricht eingeben: ").strip()
    if nachricht == "":
        print("[Fehler] Leere Nachricht.")
        return

    nachricht_zensiert = zensiere_nachricht(nachricht)
    text = f"MSG {HANDLE} {nachricht_zensiert}\n"

    try:
        verbindung, is_ipv6 = create_socket_for_ip(ip)
        if is_ipv6:
            verbindung.connect((ip, port, 0, 0))
        else:
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
        verbindung, is_ipv6 = create_socket_for_ip(ip)
        if is_ipv6:
            verbindung.connect((ip, port, 0, 0))
        else:
            verbindung.connect((ip, port))

        verbindung.sendall(header.encode("utf-8"))

        with open(pfad, "rb") as datei:
            daten = datei.read()
            verbindung.sendall(daten)

        verbindung.close()
        print("[Gesendet] Bild wurde gesendet.")
    except Exception as fehler:
        print("[Fehler] Bild konnte nicht gesendet werden:", fehler)

