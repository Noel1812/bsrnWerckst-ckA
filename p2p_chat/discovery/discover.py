// von Mulu und Milad //

import socket
import time
import threading

class DiscoveryService:
    def __init__(self, handle, port, whoisport):
        self.handle = handle
        self.port = port
        self.whoisport = whoisport
        self.peers = {}  # {(ip, port): {"handle": ..., "last_seen": ...}}
        self.running = True

    def send_join_loop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while self.running:
                message = f"JOIN:{self.handle}:{self.port}"
                s.sendto(message.encode(), ("255.255.255.255", self.whoisport))
                print(f"[Discovery] JOIN gesendet: {message}")
                time.sleep(5)

    def listen_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("0.0.0.0", self.whoisport))
        print(f"[Discovery] Lausche auf Port {self.whoisport}")

        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
                msg = data.decode().strip()
                sender_ip, _ = addr

                if msg == "WHOIS":
                    response = f"{self.handle}:{self.port}"
                    sock.sendto(response.encode(), addr)

                elif msg.startswith("JOIN:"):
                    parts = msg.split(":")
                    if len(parts) == 3:
                        peer_handle, peer_port = parts[1], int(parts[2])
                        key = (sender_ip, peer_port)
                        self.peers[key] = {
                            "handle": peer_handle,
                            "last_seen": time.time()
                        }
                        print(f"[Discovery] JOIN empfangen von {peer_handle}@{sender_ip}:{peer_port}")

                elif msg.startswith("LEAVE:"):
                    parts = msg.split(":")
                    if len(parts) == 3:
                        peer_handle, peer_port = parts[1], int(parts[2])
                        key = (sender_ip, peer_port)
                        if key in self.peers:
                            del self.peers[key]
                            print(f"[Discovery] {peer_handle}@{sender_ip}:{peer_port} hat das Netzwerk verlassen.")

            except Exception as e:
                print(f"[Discovery] Fehler beim Empfang: {e}")

    def cleanup_loop(self):
        while self.running:
            now = time.time()
            stale = [key for key, val in self.peers.items() if now - val["last_seen"] > 15]
            for key in stale:
                handle = self.peers[key]["handle"]
                print(f"[Discovery] Entferne inaktiven Peer {handle}@{key[0]}:{key[1]}")
                del self.peers[key]
            time.sleep(10)

    def start(self):
        threading.Thread(target=self.send_join_loop, daemon=True).start()
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.cleanup_loop, daemon=True).start()

    def stop(self):
        self.running = False

    def get_peers(self):
        return [f"{ip}:{port}" for (ip, port) in self.peers.keys()]

