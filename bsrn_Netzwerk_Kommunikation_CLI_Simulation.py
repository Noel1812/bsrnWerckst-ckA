# CLI Simulation - von Nurettin Tasoluk
# Grundbefehle eines Peer-to-Peer-Chats zur Vorbereitung auf die Socket-Programmierung

def start_p2p_demo():
    print("----- P2P Chat Netzwerk -----")
    print("Verfügbare Befehle: JOIN | WHO | MSG | IMG | LEAVE")
    print("Ziel: Verständnis zeigen, wie Peer-Kommunikation in Python ablaufen wird.\n")

    aktiv = True
    while aktiv:
        eingabe = input(">> Befehl eingeben: ").strip().upper()

        if eingabe == "JOIN":
            print("[System] Du trittst dem lokalen Chat-Netzwerk bei (noch ohne Verbindung).")
        elif eingabe == "WHO":
            print("[System] Aktive Peers: Peer_01, Peer_02 (simuliert)")
        elif eingabe == "MSG":
            print("[System] Nachricht wird vorbereitet zum Senden... (Netzwerklogik folgt später)")
        elif eingabe == "IMG":
            print("[System] Bildversand ist geplant, aber aktuell nicht implementiert.")
        elif eingabe == "LEAVE":
            print("[System] Verbindung getrennt. Du hast das Netzwerk verlassen.")
            aktiv = False
        else:
            print("[Fehler] Unbekannter Befehl. Bitte gültigen Befehl eingeben.")

if __name__ == "__main__":
    start_p2p_demo()
