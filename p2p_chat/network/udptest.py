# network/udp.py – Echten Broadcast senden
import socket

BROADCAST_PORT = 50000
BROADCAST_IP = '255.255.255.255'

def sende_udp_broadcast(nutzername):
    nachricht = f"JOIN:{nutzername}"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(nachricht.encode(), (BROADCAST_IP, BROADCAST_PORT))
        print(f"[Netzwerk] Broadcast gesendet: {nachricht}")
