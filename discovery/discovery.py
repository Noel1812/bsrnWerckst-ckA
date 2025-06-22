#Mulu und Milad
import socket
import time

# Diese Funktion läuft parallel und kümmert sich um das Entdecken der Peers im Netzwerk
def discovery_process(handle, port, whoisport, pipe_conn):
    peers = {}  # Hier speichern wir alle bekannten Peers mit Handle, IP, Port, usw.

    # UDP-Socket für IPv4-Broadcast erstellen
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", whoisport))  # Hört auf WHO, JOIN, LEAVE, KNOWUSERS
    print("[INFO] Discovery läuft über IPv4")

    # Lokale IP-Adresse ermitteln (nicht immer 127.0.0.1)
    try:
        tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tmp.connect(("8.8.8.8", 80))
        local_ip = tmp.getsockname()[0]
        tmp.close()
    except:
        local_ip = "127.0.0.1"

    # Sich selbst als Peer eintragen (wird bei PEERS aber oft rausgefiltert)
    peers[(local_ip, port)] = {
        "handle": handle,
        "ip": local_ip,
        "port": port,
        "last_seen": time.time()
    }

    last_send_time = 0

    while True:
        now = time.time()

        # Alle 5 Sekunden JOIN senden, damit andere einen sehen
        if now - last_send_time > 5:
            join_msg = f"JOIN:{handle}:{port}"
            try:
                sock.sendto(join_msg.encode(), ("255.255.255.255", whoisport))
            except Exception as e:
                print("[WARNUNG] JOIN fehlgeschlagen:", e)
            last_send_time = now

        sock.settimeout(1.0)  # Max. 1 Sekunde auf Antwort warten
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode().strip()
            sender_ip, sender_port = addr

            # Wenn jemand JOIN sendet → als Peer speichern
            if msg.startswith("JOIN:"):
                parts = msg.split(":")
                if len(parts) == 3:
                    peer_handle = parts[1]
                    peer_port = int(parts[2])
                    peers[(sender_ip, peer_port)] = {
                        "handle": peer_handle,
                        "ip": sender_ip,
                        "port": peer_port,
                        "last_seen": now
                    }

            # Wenn jemand LEAVE sendet → aus der Liste löschen
            elif msg.startswith("LEAVE:"):
                parts = msg.split(":")
                if len(parts) == 3:
                    peer_port = int(parts[2])
                    peers.pop((sender_ip, peer_port), None)

            # Wenn WHO empfangen wird -> eigene bekannte Peers zurücksenden
            elif msg.startswith("WHO"):
                user_entries = []
                for (ip, p), info in peers.items():
                    user_entries.append(f"{info['handle']} {ip} {p}")
                antwort = "KNOWUSERS " + ", ".join(user_entries)
                try:
                    antwort_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    antwort_sock.sendto(antwort.encode("utf-8"), addr)
                    antwort_sock.close()
                except Exception as e:
                    print("[WARNUNG] KNOWUSERS konnte nicht gesendet werden:", e)

            # Wenn KNOWUSERS empfangen → neue Peers eintragen
            elif msg.startswith("KNOWUSERS"):
                eintraege = msg[11:].split(",")
                for eintrag in eintraege:
                    teile = eintrag.strip().split(" ")
                    if len(teile) == 3:
                        peer_handle, peer_ip, peer_port = teile
                        peer_port = int(peer_port)
                        peers[(peer_ip, peer_port)] = {
                            "handle": peer_handle,
                            "ip": peer_ip,
                            "port": peer_port,
                            "last_seen": now
                        }

        # Kommt manchmal unter Windows vor, wenn WHO blockiert wird
        except ConnectionResetError as e:
            print("[WARNUNG] UDP-Antwort blockiert (Windows-Firewall?):", e)
            continue

        # Kein Paket bekommen – einfach weitermachen
        except socket.timeout:
            pass

        # Aktuelle Liste der Peers an das CLI senden (für >> PEERS Anzeige)
        # ❗ Wenn kein WHO gesendet wurde, enthält die Liste oft nur sich selbst!
        pipe_conn.send([
            f"{info['handle']} {ip}:{p}" for (ip, p), info in peers.items()
        ])
