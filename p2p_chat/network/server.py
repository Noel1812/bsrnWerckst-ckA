import socket

def empfange_nachricht(sock):
    nachricht = sock.recv(1024).decode()
    print("Nachricht empfangen:", nachricht)

def empfange_bild(sock):
    groesse = int.from_bytes(sock.recv(4), 'big')  
    daten = b""
    while len(daten) < groesse:
        daten += sock.recv(1024)
    with open("empfangenes_bild.jpg", "wb") as f:
        f.write(daten)
    print("Bild empfangen und gespeichert!")

server = socket.socket()
server.bind(("", 5000))  
server.listen(1)         

print("Server läuft und wartet auf Daten...")

while True:
    conn, addr = server.accept()
    print("Verbindung von", addr)
    code = conn.recv(4).decode()

    if code == "MSG:":
        empfange_nachricht(conn)
    elif code == "IMG:":
        empfange_bild(conn)
    else:
        print("Unbekannte Nachricht:", code)

    conn.close()

if __name__ == "__main__":
    print("Server wird beendet.")
    server.close()
    