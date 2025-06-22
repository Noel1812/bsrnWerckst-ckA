import socket
from network.client import send_msg, send_image  # Noel client.py importieren

def run_cli(handle, port, whoisport, pipe_conn): 
    """
    Startet die Kommandozeilenoberfläche für den P2P-Chat.
    
    :param handle: Nutzername
    :param port: Lokaler TCP-Port für den Server
    :param whoisport: UDP-Port für Discovery-Broadcasts
    :param pipe_conn: Verbindung zur Discovery-Pipe (für Peer-Listen)
    """
    print("Verfügbare Befehle: PEERS | MSG | IMG | JOIN | LEAVE | WHO | BEENDEN")

    try:
        while True:
            # Hier wird der Benutzer eingegeben
            cmd = input(">> ").strip().upper() 

            if cmd == "PEERS": 
                # Prüft ob neue Peer-Daten verfügbar sind 
                if pipe_conn.poll(1):  
                    peers = pipe_conn.recv()  # Empfange Peer-Liste
                    if peers:
                        print(" Aktive Peers:")
                        for peer in peers:
                            print(f" - {peer}")
                    else:
                        print(" Keine aktiven Peers gefunden.")
                else:
                    print(" Keine neuen Peer-Daten verfügbar.")

            elif cmd == "MSG":
                # Manuelle Eingabe von IP und Port vom Empfänger 
                ip = input("Peer-IP: ").strip()
                port_str = input("Peer-Port: ").strip() 
                send_msg(ip, int(port_str))  # Nachricht über TCP senden

            elif cmd == "IMG":
                ip = input("Peer-IP: ").strip()
                port_str = input("Peer-Port: ").strip()
                send_image(ip, int(port_str))  # Bild über TCP senden

            elif cmd == "JOIN":
                # JOIN-Nachricht über UDP-Broadcast verschicken
                join_msg = f"JOIN:{handle}:{port}"
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Erstelle UDP-Socket
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Aktiviere Broadcast
                sock.sendto(join_msg.encode(), ("255.255.255.255", whoisport))  # Sende an Netzwerk
                sock.close()
                print(" JOIN-Nachricht gesendet.")

            elif cmd == "LEAVE":
                # LEAVE-Nachricht über UDP-Broadcast verschicken und CLI verlassen
                leave_msg = f"LEAVE:{handle}:{port}"
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(leave_msg.encode(), ("255.255.255.255", whoisport))
                sock.close()
                print(" Du hast den Chat verlassen.")
                break  # Beende CLI

            elif cmd == "WHO":
                # Sende WHO-Anfrage über UDP-Broadcast
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                try:
                    sock.sendto(b"WHO", ("255.255.255.255", whoisport)) 
                    print(" WHO-Nachricht gesendet.")
                except Exception as e:
                    print("[Fehler] WHO konnte nicht gesendet werden:", e)
                finally:
                    sock.close()

            elif cmd == "BEENDEN":
                # Beende CLI ohne LEAVE
                print(" CLI wird beendet.")
                break

            else:
                # Ungültiger Befehl
                print(" Ungültiger Befehl. Versuche: PEERS | MSG | IMG | JOIN | LEAVE | WHO | BEENDEN")

    except KeyboardInterrupt:
        # CLI mit Strg+C beendet
        print("\n[INFO] Manuelle Beendigung durch Benutzer (Strg+C).")


