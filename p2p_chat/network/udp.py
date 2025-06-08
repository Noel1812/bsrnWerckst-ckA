# UDP Broadcast – P2P Chat von Nurettin Tasoluk 
# JOIN-Befehl sendet jetzt echten UDP-Broadcast ins lokale Netzwerk

import socket

BROADCAST_PORT = 50000  # Standardport für Discovery
BROADCAST_IP = '255.255.255.255'  # UDP-Broadcast-Adresse
BENUTZERNAME = "Nurettin"

def sende_udp_broadcast(nutzername):
    """
    Sendet eine UDP-Nachricht an alle im lokalen Netzwerk (Broadcast),
    um anderen Peers mitzuteilen: 'Ich bin online!'
    """
    nachricht = f"JOIN:{nutzername}"
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Broadcast aktivieren
        s.sendto(nachricht.encode(), (BROADCAST_IP, BROADCAST_PORT))
        print(f"[Netzwerk] Broadcast gesendet: {nachricht}")

def start_p2p_demo():
    print("----- P2P Chat Netzwerk UDB Broadcast -----")
    print("Verfügbare Befehle: JOIN | WHO | MSG | IMG | LEAVE")
    print("Hinweis: JOIN sendet echten UDP-Broadcast.\n")

    aktiv = True
    while aktiv:
        befehl = input(">> Befehl eingeben: ").strip().upper()

        if befehl == "JOIN":
            sende_udp_broadcast(BENUTZERNAME)
        elif befehl == "WHO":
            print("[System] WHO-Befehl später: erfordert Peer-Liste (noch nicht vorhanden)")
        elif befehl == "MSG":
            print("[System] MSG simuliert nur – Netzwerkversand kommt später.")
        elif befehl == "IMG":
            print("[System] Bildversand ist geplant – aktuell deaktiviert.")
        elif befehl == "LEAVE":
            print("[System] Verbindung getrennt. Du verlässt das Netzwerk.")
            aktiv = False
        else:
            print("[Fehler] Unbekannter Befehl. Gültig: JOIN, WHO, MSG, IMG, LEAVE")

if __name__ == "__main__":
    start_p2p_demo()
