import socket

def send_message(message, peer_ip, peer_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (peer_ip, peer_port))
    sock.close()

def start_listening(my_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", my_port))
    print(f" Warte auf Nachrichten auf Port {my_port}...")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Nachricht von {addr}: {data.decode()}")
