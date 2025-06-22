import socket
import threading
import os
import time

def start_server(port, autoreply, imagepath, handle):
    def server_thread():
        if not os.path.exists(imagepath):
            os.makedirs(imagepath)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", port))
            s.listen(5)
            print(f"[TCP-Server] Lauscht auf Port {port} (IPv4) ...")

            while True:
                conn, addr = s.accept()
                threading.Thread(target=handle_connection, args=(conn, addr), daemon=True).start()

    def handle_connection(conn, addr):
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
                        conn.sendall(reply.encode("utf-8"))  # direkt über bestehende Verbindung antworten

                elif data.startswith("IMG"):
                    header = data.split(" ")
                    if len(header) == 3:
                        _, sender, size_str = header
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
            except Exception as e:
                print(f"[Fehler beim Empfangen] {e}")

    thread = threading.Thread(target=server_thread, daemon=True)
    thread.start()
