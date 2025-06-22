Milad
# main.py

import os
from multiprocessing import Process, Pipe
from config.loader import load_config
from network.cli import run_cli
from network.server import start_server
from discovery.discovery import discovery_process

def main():
    # Die Konfiguration aus der gewünschten settingsX.toml-Datei werden geladen
    # Diese Datei muss manuell angepasst werden, je nachdem welcher User gerade aktiv ist
    # Beispiel: settings3.toml für Milad, settings1.toml für Noel, usw.
    config = load_config("config/settings4.toml")  # Hier ggf. andere Datei wählen

    handle = config["handle"]
    port = config["port"]
    whoisport = config["whoisport"]
    autoreply = config["autoreply"]
    imagepath = config["imagepath"]

    # Startet den TCP-Server, der eingehende Nachrichten und Bilder empfängt
    # Im Hintergrund läuft – CLI & Discovery können parallel genutzt werden
    start_server(port, autoreply, imagepath, handle)

    # Starte den Discovery-Prozess separat, damit er ständig JOIN & WHO Nachrichten verarbeiten kann
    # Die Kommunikation zur CLI erfolgt über der Pipe
    parent_conn, child_conn = Pipe()
    discovery = Process(target=discovery_process, args=(handle, port, whoisport, child_conn))
    discovery.start()

    # Startet die Kommandozeilen-Oberfläche (CLI), über die man z. B. PEERS, MSG, IMG usw. ausführen kann
    run_cli(handle, port, whoisport, parent_conn)

    # Sobald die CLI beendet wird, Discovery-Prozess ordentlich beenden
    discovery.terminate()
    discovery.join()

# Dieser Teil sorgt dafür, dass das Programm nur startet,
# wenn wir die Datei direkt ausführen (nicht beim Importieren).
# So verhindern wir, dass z. B. beim Testen automatisch Server oder Discovery loslaufen.
if __name__ == "__main__":
    main()
