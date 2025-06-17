import socket
import os

def run_cli(handle, port, whoisport, pipe_conn):
    """
    Interaktive Kommandozeile für Benutzerbefehle.
    Verarbeitet: PEERS, MSG, IMG, LEAVE, BEENDEN.
    Kommuniziert über pipe_conn mit dem Discovery-Prozess.
    """
    print("Verfügbare Befehle: PEERS | MSG | IMG | LEAVE | BEENDEN")
    
    try:
        while True:
            cmd = input(">> ").strip().upper()

            if cmd == "PEERS":
                # Zeige Peer-Liste, falls verfügbar
                if pipe_conn.poll(1):
                    peers = pipe_conn.recv()
                    if peers:
                        print(" Aktive Peers:")
                        for peer in peers:
                            print(f" - {peer}")
                    else:
                        print(" Keine aktiven Peers gefunden.")
                else:
                    print(" Keine neuen Peer-Daten verfügbar.")

            elif cmd == "MSG":
                # Nachricht an Peer senden
                ip = input("Peer-IP: ").strip()
                port_str = input("Peer-Port: ").strip()
                msg = input("Nachricht: ").strip()
                send_message(f"{handle}: {msg}", ip, int(port_str))

            elif cmd == "IMG":
                # Bild an Peer senden
                ip = input("Peer-IP: ").strip()
                port_str = input("Peer-Port: ").strip()
                filepath = input("Pfad zum Bild: ").strip()
                send_image(filepath, ip, int(port_str), handle)

            elif cmd == "LEAVE":
                # LEAVE-Broadcast senden und beenden
                leave_msg = f"LEAVE:{handle}:{port}"
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(leave_msg.encode(), ("255.255.255.255", whoisport))
                sock.close()
                print(" Du hast den Chat verlassen.")
                break

            elif cmd == "BEENDEN":
                print(" CLI wird beendet.")
                break

            else:
                print(" Ungültiger Befehl. Versuche: PEERS | MSG | IMG | LEAVE | BEENDEN")

    except KeyboardInterrupt:
        print("\n[INFO] Manuelle Beendigung durch Benutzer (Strg+C).")
