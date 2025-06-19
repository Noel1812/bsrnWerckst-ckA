# Mulu und Milad

import socket
import time
from multiprocessing import Process, Pipe

def discovery_process(handle, port, whoisport, pipe_conn):
    peers = {}  # {(ip, port): {"handle": ..., "ip": ..., "port": ...}}

    # UDP-Socket vorbereiten
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", whoisport))

    # Eigene IP herausfinden (robust)
    try:
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_sock.connect(("8.8.8.8", 80))
        local_ip = temp_sock.getsockname()[0]
        temp_sock.close()
    except Exception:
        local_ip = "127.0.0.1"

    # Sich selbst zur Peer-Liste hinzufügen
    peers[(local_ip, port)] = {
        "handle": handle,
        "ip": local_ip,
        "port": port
    }

    while True:
        sock.settimeout(1.0)
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode().strip()
            sender_ip, _ = addr

            if msg == "WHOIS" or msg == "WHO":
                # Antwort im Format: KNOWNUSERS <Handle1> <IP1> <Port1>, ...
                response = "KNOWNUSERS"
                for (ip, p), info in peers.items():
                    response += f" {info['handle']} {ip} {p},"
                response = response.rstrip(',')
                sock.sendto(response.encode(), addr)

            elif msg.startswith("JOIN:"):
                parts = msg.split(":")
                if len(parts) == 3:
                    peer_handle = parts[1]
                    peer_port = int(parts[2])
                    key = (sender_ip, peer_port)
                    peers[key] = {
                        "handle": peer_handle,
                        "ip": sender_ip,
                        "port": peer_port
                    }

            elif msg.startswith("LEAVE:"):
                parts = msg.split(":")
                if len(parts) == 3:
                    peer_handle, peer_port = parts[1], int(parts[2])
                    key = (sender_ip, peer_port)
                    if key in peers:
                        del peers[key]

        except socket.timeout:
            pass

        # Peer-Liste an Hauptprozess senden (z. B. CLI)
        pipe_conn.send([
            f"{val['handle']} {ip}:{port}" for (ip, port), val in peers.items()
        ])
