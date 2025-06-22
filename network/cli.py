import socket
from network.client import send_msg, send_image  # Noels Funktion aus client.py

def run_cli(handle, port, whoisport, pipe_conn):
    print("Verfügbare Befehle: PEERS | MSG | IMG | JOIN | LEAVE | WHO | BEENDEN")

    try:
        while True:
            cmd = input(">> ").strip().upper()

            if cmd == "PEERS":
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
                ip = input("Peer-IP: ").strip()
                port_str = input("Peer-Port: ").strip()
                send_msg(ip, int(port_str))

            elif cmd == "IMG":
                ip = input("Peer-IP: ").strip()
                port_str = input("Peer-Port: ").strip()
                send_image(ip, int(port_str))

            elif cmd == "JOIN":
                join_msg = f"JOIN:{handle}:{port}"
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(join_msg.encode(), ("255.255.255.255", whoisport))
                sock.close()
                print(" JOIN-Nachricht gesendet.")

            elif cmd == "LEAVE":
                leave_msg = f"LEAVE:{handle}:{port}"
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(leave_msg.encode(), ("255.255.255.255", whoisport))
                sock.close()
                print(" Du hast den Chat verlassen.")
                break

            elif cmd == "WHO":
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
                print(" CLI wird beendet.")
                break

            else:
                print(" Ungültiger Befehl. Versuche: PEERS | MSG | IMG | JOIN | LEAVE | WHO | BEENDEN")

    except KeyboardInterrupt:
        print("\n[INFO] Manuelle Beendigung durch Benutzer (Strg+C).")
