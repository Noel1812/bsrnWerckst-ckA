import socket
import time
from config.loader import load_config

def discovery_process(pipe_conn):
    config = load_config("config/settings1.toml")  # Je nach Client ändern
    handle = config["handle"]
    port = config["port"]
    whoisport = config["whoisport"]

    peers = {}  # {(ip, port): {...}}

    # IPv6 bevorzugen, bei Fehler auf IPv4 zurückfallen
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("::", whoisport))
        print("[INFO] Discovery läuft über IPv6")
    except Exception as e:
        print("[WARNUNG] IPv6 fehlgeschlagen, wechsle zu IPv4:", e)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("0.0.0.0", whoisport))
        print("[INFO] Discovery läuft über IPv4")

    # Lokale IP ermitteln
    try:
        tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tmp.connect(("8.8.8.8", 80))
        local_ip = tmp.getsockname()[0]
        tmp.close()
    except:
        local_ip = "127.0.0.1"

    peers[(local_ip, port)] = {
        "handle": handle,
        "ip": local_ip,
        "port": port,
        "last_seen": time.time()
    }

    last_send_time = 0

    while True:
        now = time.time()

        # Regelmäßig JOIN senden
        if now - last_send_time > 5:
            join_msg = f"JOIN:{handle}:{port}"
            try:
                if sock.family == socket.AF_INET6:
                    sock.sendto(join_msg.encode(), ("ff02::1", whoisport))
                else:
                    sock.sendto(join_msg.encode(), ("255.255.255.255", whoisport))
            except Exception as e:
                print("[WARNUNG] JOIN fehlgeschlagen:", e)
            last_send_time = now

        sock.settimeout(1.0)
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode().strip()

            if sock.family == socket.AF_INET6:
                sender_ip = addr[0]
                sender_port = addr[1]
            else:
                sender_ip, sender_port = addr

            if msg == "WHOIS" or msg == "WHO":
                response = "KNOWNUSERS"
                for (ip, p), info in peers.items():
                    response += f" {info['handle']} {ip} {p},"
                response = response.rstrip(",")
                sock.sendto(response.encode(), addr)

            elif msg.startswith("JOIN:"):
                parts = msg.split(":")
                if len(parts) == 3:
                    peer_handle = parts[1]
                    peer_port = int(parts[2])
                    peers[(sender_ip, peer_port)] = {
                        "handle": peer_handle,
                        "ip": sender_ip,
                        "port": peer_port,
                        "last_seen": now
                    }

            elif msg.startswith("LEAVE:"):
                parts = msg.split(":")
                if len(parts) == 3:
                    peer_port = int(parts[2])
                    key = (sender_ip, peer_port)
                    if key in peers:
                        del peers[key]

        except socket.timeout:
            pass

        # Inaktive Peers entfernen
        for key in list(peers.keys()):
            if now - peers[key]["last_seen"] > 15:
                del peers[key]

        # Aktuelle Peers an CLI schicken
        pipe_conn.send([
            f"{info['handle']} {ip}:{p}" for (ip, p), info in peers.items()
        ])
