from network.messaging import sende_nachricht, sende_bilddatei

def start_ui():
    print("===== P2P Chat =====")
    print("Verfügbare Befehle: MSG | IMG | EXIT")
    while True:
        befehl = input(">> ").strip().upper()
        if befehl == "MSG":
            text = input("Nachricht: ")
            sende_nachricht(text)
        elif befehl == "IMG":
            pfad = input("Pfad zur Bilddatei: ")
            sende_bilddatei(pfad)
        elif befehl == "EXIT":
            print("[System] Chat beendet.")
            break
        else:
            print("Unbekannter Befehl. Verwende MSG, IMG oder EXIT.")

if __name__ == "__main__":
    start_ui()