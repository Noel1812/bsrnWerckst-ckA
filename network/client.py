import socket
import os
from config.loader import load_config

##
# @file client.py
# @brief Dieses Programm sendet Textnachrichten und Bilder über TCP/IP im lokalen Netzwerk.
#
# Das war ein weiterer Teil (Noel) des Peer-to-Peer Chat-Projekts. Ich habe diesen Client gebaut, damit
# man mit anderen Peers über IP kommunizieren kann – entweder mit Text oder mit einem Bild.
#
# Ursprünglich hatte ich Unterstützung für IPv6 drin, aber das hat bei meinem Kommilitonen 
# nicht zuverlässig funktioniert (wir hatten oft `No route to host` oder `Connection refused`) 
# obwohl wir die richtigen Adressen verwendet haben. 
# Deshalb habe ich den Code zurück auf IPv4 reduziert – das ist einfacher, stabiler und wir 
# hatten damit weniger Probleme.
#
# Außerdem war es schwer, bei IPv6 richtige Adressen zu bekommen, die auf beiden Rechnern 
# funktionieren. Wir haben viel Zeit mit `ip addr show` und `ipconfig` verbracht, aber ohne Erfolg.  
# Zwischenzeitlich konnte ich zwar Textnachrichten senden, aber mein Kommilitone konnte nicht antworten.  
# IPv4 war letztendlich einfach klarer und zuverlässiger.

## @var config
# Lädt Konfigurationswerte aus der TOML-Datei
config = load_config("config/settings3.toml")
HANDLE = config["handle"]       
PORT = config["port"]             
WHOISPORT = config["whoisport"]    
AUTOREPLY = config["autoreply"]    
IMAGEPATH = config["imagepath"] 

BUFFER_SIZE = 4096  

##
# @brief Liste mit Wörtern, die in Nachrichten zensiert werden sollen.
#
# Die Idee kam uns in einer ihrer Übungen und hat uns ein wenig an Exceptions aus Java erinnert.
# Wir wollten eine einfache Möglichkeit, beleidigende Wörter in Nachrichten zu ersetzen.
# Die Liste ist beliebig erweiterbar, falls wir später noch mehr Wörter zensieren wollen.
#
BLACKLIST = [
    "arschloch", "penner", "fuck", "idiot", "dummkopf", "arsch",
    "spast", "miststück", "arschh", "fuckk", "scheiße", "fick dich"
]

##
# @brief Ersetzt beleidigende Wörter mit Sternchen.
# 
# @param text Der Original-Text, den der Nutzer geschrieben hat.
# @return Eine zensierte Version des Texts.
#
def zensiere_nachricht(text):
    for wort in BLACKLIST:
        maskiert = "*" * len(wort)
        text = text.replace(wort, maskiert).replace(wort.capitalize(), maskiert)
    return text

##
# @brief Sendet eine Textnachricht an einen Peer über IPv4.
#
# @param ip Die Ziel-IP-Adresse des Empfängers.
# @param port Der Port, an dem der Empfänger zuhört.
#
# @note Die Nachricht wird über die Konsole eingegeben.
#       Bevor gesendet wird, zensiere ich sie automatisch.
#
def send_msg(ip, port):
    nachricht = input("Nachricht eingeben: ").strip()
    if nachricht == "":
        print("[Fehler] Leere Nachricht.")
        return

    nachricht_zensiert = zensiere_nachricht(nachricht)
    text = f"MSG {HANDLE} {nachricht_zensiert}\n"

    try:
        verbindung = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        verbindung.connect((ip, port))
        verbindung.sendall(text.encode("utf-8"))
        verbindung.close()
        print("[Gesendet] Nachricht wurde gesendet.")
    except Exception as fehler:
        print("[Fehler] Nachricht konnte nicht gesendet werden:", fehler)

##
# @brief Sendet eine Bilddatei an einen Peer über IPv4.
#
# @param ip Die Ziel-IP-Adresse des Empfängers.
# @param port Der Port, an dem der Empfänger lauscht.
#
# @note Der Pfad zum Bild wird über die Konsole eingegeben.
#       Das Bild wird vollständig als Binärdaten gesendet.
#
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

