import socket
import time

def discovery_process(handle, port, whoisport, pipe_conn):
    peers = {}

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", whoisport))
    print("[INFO] Discovery läuft über IPv4")

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

        if now - last_send_time > 5:
            join_msg = f"JOIN:{handle}:{port}"
            try:
                sock.sendto(join_msg.encode(), ("172.20.10.255", whoisport))
            except Exception as e:
                print("[WARNUNG] JOIN fehlgeschlagen:", e)
            last_send_time = now

        sock.settimeout(1.0)
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode().strip()
            sender_ip, sender_port = addr

            if msg.startswith("JOIN:"):
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
                    peers.pop((sender_ip, peer_port), None)

        except socket.timeout:
            pass

        pipe_conn.send([
            f"{info['handle']} {ip}:{p}" for (ip, p), info in peers.items()
        ])
