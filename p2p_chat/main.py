from config.loader import load_config
from network.messaging import send_message, start_listening
import threading

# Datei aus settings.toml einlesen
import sys

# Optional: Dateiname per Argument übergeben
config_path = sys.argv[1] if len(sys.argv) > 1 else "config/settings.toml"
config = load_config(config_path)

handle = config["handle"]
my_port = config["port"]
peers = config["peers"]

#  Konfiguration ausgeben 
print("Handle:", handle)
print("Port:", my_port)
print("Peers:", peers)
print("Starte Listener...")

# listener
threading.Thread(target=start_listening, args=(my_port,), daemon=True).start()

# while schleife um Nachrichten einzugeben 
print("Gib eine Nachricht ein (oder 'exit' zum Beenden):")
while True:
    message = input("> ")
    if message == "exit":
        break

    full_message = f"{handle}: {message}"
    for peer in peers:
        ip, port = peer.split(":")
        send_message(full_message, ip, int(port))




# Verknüpfung mit Discovery (eventuell)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
leave_msg = f"LEAVE:{handle}:{port}"
sock.sendto(leave_msg.encode(), ("255.255.255.255", whoisport))

