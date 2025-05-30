import socket

def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0

def send_message(ip, port, msg):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.send(msg.encode())
        s.close()
    except Exception as e:
        print(f"⚠️  Fehler beim Senden an {ip}:{port} → {e}")

def start_server(port):
    if not is_port_available(port):
        print(f"❌ Port {port} ist bereits belegt.")
        return

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))
    s.listen()
    while True:
        conn, addr = s.accept()
        print(f"[{addr}] {conn.recv(1024).decode()}")
        conn.close()

def network_loop(queue, config_path):
    import tomli
    with open(config_path, "rb") as f:
        config = tomli.load(f)
    port = config["port"]

    import threading
    server_thread = threading.Thread(target=start_server, args=(port,))
    server_thread.start()

    while True:
        user, message = queue.get()
        ip, port = user.split(":")
        send_message(ip, int(port), message)
