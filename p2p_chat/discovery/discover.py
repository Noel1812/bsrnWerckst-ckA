# Mulu und Milad

import socket
import time
from multiprocessing import Process, Pipe

def discovery_process(handle, port, whoisport, pipe_conn):
    peers = {}  # {(ip, port): {"handle": ..., "last_seen": ...}}

    # Setup Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", whoisport))

    last_send_time = 0

    while True:
        now = time.time()

        # Regelmäßig JOIN senden
        if now - last_send_time > 5:
            message = f"JOIN:{handle}:{port}"
            sock.sendto(message.encode(), ("255.255.255.255", whoisport))
            last_send_time = now

        # Nachrichten empfangen
        sock.settimeout(1.0)
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode().strip()
            sender_ip, _ = addr

            if msg == "WHOIS":
                response = f"{handle}:{port}"
                sock.sendto(response.encode(), addr)

            elif msg.startswith("JOIN:"):
                parts = msg.split(":")
                if len(parts) == 3:
                    peer_handle, peer_port = parts[1], int(parts[2])
                    key = (sender_ip, peer_port)
                    peers[key] = {
                        "handle": peer_handle,
                        "last_seen": now
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

        # Alte Peers entfernen
        stale = [key for key, val in peers.items() if now - val["last_seen"] > 15]
        for key in stale:
            del peers[key]

        # Peer-Liste regelmäßig an Hauptprozess senden
        pipe_conn.send([f"{ip}:{port}" for (ip, port) in peers.keys()])

