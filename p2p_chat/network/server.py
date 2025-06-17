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
    print("Bild gespeichert als empfangenes_bild.jpg")

# Server starten
server = socket.socket()
server.bind(("", 5000))
server.listen(1)

print("Warte auf Nachrichten oder Bilder...")

while True:
    conn, addr = server.accept()
    print("Verbunden mit", addr)
    code = conn.recv(4).decode()

    if code == "MSG:":
        empfange_nachricht(conn)
    elif code == "IMG:":
        empfange_bild(conn)

    conn.close()
