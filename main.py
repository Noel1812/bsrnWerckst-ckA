# main.py
import os
from multiprocessing import Process, Pipe
from config.loader import load_config
from network.cli import run_cli
from network.server import start_server
from discovery.discovery import discovery_process

def main():
    # Konfiguration laden
    config = load_config("config/settings4.toml")  # Ändere hier ggf. settings2.toml etc.
    handle = config["handle"]
    port = config["port"]
    whoisport = config["whoisport"]
    autoreply = config["autoreply"]
    imagepath = config["imagepath"]

    # Starte den TCP-Server (empfängt Nachrichten & Bilder)
    start_server(port, autoreply, imagepath, handle)

    # Starte Discovery-Prozess (eigenständiger Prozess mit Pipe zur CLI)
    parent_conn, child_conn = Pipe()
    discovery = Process(target=discovery_process, args=(handle, port, whoisport, child_conn))
    discovery.start()

    # Starte CLI (interaktive Eingabe)
    run_cli(handle, port, whoisport, parent_conn)

    # Wenn CLI endet → Discovery-Prozess beenden
    discovery.terminate()
    discovery.join()

if __name__ == "__main__":
    main()