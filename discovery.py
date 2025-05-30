import toml
import socket
import time
import threading
import multiprocessing

# ...restlicher Code...

# Konfiguration aus TOML-Datei lesen
def read_config(file_path="config.toml"):
    config = toml.load(file_path)
    return config["handle"], config["whoisport"]

# UDP-Broadcast senden
def broadcast_loop(handle, whois_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = f"SLCP DISCOVERY {handle}"

    while True:
        s.sendto(message.encode(), ("<broadcast>", whois_port))
        time.sleep(5)

# UDP-Nachrichten empfangen und Peer-Liste pflegen
def listen_loop(whois_port, peer_list):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', whois_port))

    while True:
        data, addr = s.recvfrom(1024)
        message = data.decode()

        if message.startswith("SLCP DISCOVERY"):
            handle = message.split(" ")[-1]
            ip = addr[0]
            peer_list[ip] = {"handle": handle, "last_seen": time.time()}

# Alte Peers nach Timeout löschen
def cleanup_loop(peer_list, timeout=30):
    while True:
        now = time.time()
        to_delete = [ip for ip, data in peer_list.items() if now - data["last_seen"] > timeout]
        for ip in to_delete:
            del peer_list[ip]
        time.sleep(10)

# Discovery-Dienst starten
def start_discovery():
    handle, whois_port = read_config()
    manager = multiprocessing.Manager()
    peer_list = manager.dict()

    threading.Thread(target=broadcast_loop, args=(handle, whois_port), daemon=True).start()
    threading.Thread(target=listen_loop, args=(whois_port, peer_list), daemon=True).start()
    threading.Thread(target=cleanup_loop, args=(peer_list,), daemon=True).start()

    while True:
        print("\n--- Aktive Peers ---")
        for ip, data in peer_list.items():
            print(f"{data['handle']} @ {ip}")
        time.sleep(5)
