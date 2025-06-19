import socket
import time
import struct
import threading
import os
from multiprocessing import Process, Pipe

def setup_ipv6_discovery_socket(whoisport):
    sock6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    sock6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock6.bind(('::', whoisport))
    
    # Multicast Interface Index (explizit: eth0, fallback auf 0)
    try:
        interface_index = socket.if_nametoindex('eth0')
    except OSError:
        interface_index = 0

    group = socket.inet_pton(socket.AF_INET6, 'ff02::1')
    mreq = group + struct.pack('@I', interface_index)
    sock6.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
    return sock6

def discovery_process(handle, port, whoisport, pipe_conn):
    peers = {}  # {(ip, port): {"handle": ..., "ip": ..., "port": ...}}

    # IPv4 Discovery Socket
    sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock4.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock4.bind(("0.0.0.0", whoisport))

    # IPv6 Discovery Socket
    sock6 = setup_ipv6_discovery_socket(whoisport)

    sockets = [sock4, sock6]

    # Eigene IP ermitteln
    try:
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_sock.connect(("8.8.8.8", 80))
        local_ip = temp_sock.getsockname()[0]
        temp_sock.close()
    except Exception:
        local_ip = "127.0.0.1"

    peers[(local_ip, port)] = {"handle": handle, "ip": local_ip, "port": port}

    while True:
        readable, _, _ = socket.select(sockets, [], [], 1.0)
        for sock in readable:
            try:
                data, addr = sock.recvfrom(1024)
                msg = data.decode("utf-8", errors="ignore").strip()
                sender_ip, _ = addr[:2]

                if msg in ("WHOIS", "WHO"):
                    response = "KNOWNUSERS"
                    for (ip, p), info in peers.items():
                        response += f" {info['handle']} {ip} {p},"
                    response = response.rstrip(',')
                    sock.sendto(response.encode("utf-8"), addr)

                elif msg.startswith("JOIN:"):
                    parts = msg.split(":")
                    if len(parts) == 3:
                        peer_handle = parts[1]
                        peer_port = int(parts[2])
                        peers[(sender_ip, peer_port)] = {
                            "handle": peer_handle,
                            "ip": sender_ip,
                            "port": peer_port
                        }

                elif msg.startswith("LEAVE:"):
                    parts = msg.split(":")
                    if len(parts) == 3:
                        peer_port = int(parts[2])
                        peers.pop((sender_ip, peer_port), None)

            except socket.timeout:
                pass

        pipe_conn.send([
            f"{val['handle']} {ip}:{port}" for (ip, port), val in peers.items()
        ])

def start_server(port, autoreply, imagepath, handle):
    def server_thread():
        if not os.path.exists(imagepath):
            os.makedirs(imagepath)

        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            s.bind(("::", port))
            s.listen(5)
            print(f"[TCP-Server] Lauscht auf Port {port} (Dual Stack) ...")

            while True:
                conn, addr = s.accept()
                with conn:
                    try:
                        data = conn.recv(1024).decode("utf-8", errors="ignore").strip()
                        if data.startswith("MSG"):
                            parts = data.split(" ", 2)
                            if len(parts) == 3:
                                _, sender, message = parts
                                print(f"\n[Nachricht von {sender}] {message}")
                                if autoreply:
                                    reply = f"MSG {handle} {autoreply}\n"
                                    reply_sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                                    reply_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
                                    try:
                                        reply_sock.connect((addr[0], addr[1]))
                                        reply_sock.sendall(reply.encode("utf-8"))
                                    except Exception as e:
                                        print(f"[Autoreply-Fehler] {e}")
                                    finally:
                                        reply_sock.close()

                        elif data.startswith("IMG"):
                            header = data.split(" ")
                            if len(header) == 3:
                                _, sender, size_str = header
                                try:
                                    size = int(size_str)
                                    img_data = b""
                                    while len(img_data) < size:
                                        chunk = conn.recv(min(4096, size - len(img_data)))
                                        if not chunk:
                                            break
                                        img_data += chunk
                                    filename = os.path.join(imagepath, f"bild_{int(time.time())}.jpg")
                                    with open(filename, "wb") as f:
                                        f.write(img_data)
                                    print(f"\n[Empfangenes Bild von {sender}] gespeichert als {filename}")
                                except ValueError:
                                    print("[Fehler] Ungültiger IMG-Header: Größe konnte nicht interpretiert werden.")
                    except Exception as e:
                        print(f"[Fehler beim Empfangen] {e}")

    thread = threading.Thread(target=server_thread, daemon=True)
    thread.start()