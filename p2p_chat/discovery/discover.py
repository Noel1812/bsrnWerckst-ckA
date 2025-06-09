import socket
import time
import tomllib


def is_udp_port_available(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("0.0.0.0", port))
        s.close()
        return True
    except:
        return False


def discovery_loop(config_path):
    # Konfiguration laden
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    whoisport = config["whoisport"]
    handle = config["handle"]
    port = config["port"]
    peers = {}

    # UDP-Socket einrichten
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("0.0.0.0", whoisport))
    print("[DISCOVERY] Dienst gestartet.")

    # Beim Start: automatisch JOIN senden
    join_message = f"JOIN {handle} {port}".encode()
    s.sendto(join_message, ("255.255.255.255", whoisport))
    print(f"[DISCOVERY] JOIN gesendet: {join_message.decode()}")

    while True:
        data, addr = s.recvfrom(1024)
        message = data.decode().strip()
        sender_ip = addr[0]

        if message == "WHOIS":
            response = f"{handle}|127.0.0.1|{port}".encode()
            s.sendto(response, addr)

        elif message.startswith("JOIN"):
            try:
                _, peer_handle, peer_port = message.split()
                peers[sender_ip] = {
                    "handle": peer_handle,
                    "port": int(peer_port),
                    "last_seen": time.time()
                }
                print(f"[DISCOVERY] {peer_handle} JOINED von {sender_ip}:{peer_port}")
            except ValueError:
                print("[DISCOVERY] Fehlerhafte JOIN-Nachricht.")

        elif message.startswith("LEAVE"):
            try:
                _, peer_handle = message.split()
                if sender_ip in peers:
                    del peers[sender_ip]
                    print(f"[DISCOVERY] {peer_handle} LEFT {sender_ip}")
            except ValueError:
                print("[DISCOVERY] Fehlerhafte LEAVE-Nachricht.")


