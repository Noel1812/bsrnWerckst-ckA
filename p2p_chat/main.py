import sys
import socket
import threading
from config.loader import load_config
from network.messaging import send_message, send_image, start_listening

# Konfiguration laden (optional über Argument)
config_path = sys.argv[1] if len(sys.argv) > 1 else "config/settings.toml"
config = load_config(config_path)

handle = config["handle"]
port = config["port"]
peers = config["peers"]
whoisport = config.get("whoisport", 6000)

print("Handle:", handle)
print("Port:", port)
print("Peers:", peers)
print("Starte Listener...")

# Starte TCP-Server im Hintergrund
threading.Thread(target=start_listening, args=(port,), daemon=True).start()

# Eingabe-Schleife
print("Gib eine Nachricht ein (Text oder '/send pfad/zum/bild.jpg', 'exit' zum Beenden):")
while True:
    message = input("> ")
    if message.strip().lower() == "exit":
        break

    if message.startswith("/send "):
        # Bildpfad extrahieren
        pfad = message.split(" ", 1)[1]
        for peer in peers:
            ip, peer_port = peer.split(":")
            try:
                send_image(pfad, ip, int(peer_port))
                print(f"[Bild] Gesendet an {ip}:{peer_port}")
            except Exception as e:
                print(f"[Fehler] Konnte Bild nicht senden: {e}")
    else:
        full_msg = f"{handle}: {message}"
        for peer in peers:
            ip, peer_port = peer.split(":")
            try:
                send_message(full_msg, ip, int(peer_port))
            except Exception as e:
                print(f"[Fehler] Nachricht nicht gesendet: {e}")

# Abschließend LEAVE-Nachricht senden
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
leave_msg = f"LEAVE:{handle}:{port}"
sock.sendto(leave_msg.encode(), ("255.255.255.255", whoisport))
print("[Discovery] LEAVE gesendet. Beende Programm.")
