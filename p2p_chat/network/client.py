import socket
import os

def sende_nachricht(text):
    sock = socket.socket()
    sock.connect(("127.0.0.1", 5000)) 
    sock.send(b"MSG:")                 
    sock.send(text.encode())          
    sock.close()
    print("Nachricht gesendet!")

def sende_bild(pfad):
    if not os.path.exists(pfad):
        print("Datei existiert nicht!")
        return

    with open(pfad, "rb") as f:
        daten = f.read()

    sock = socket.socket()
    sock.connect(("127.0.0.1", 5000)) 
    sock.send(b"IMG:")             
    sock.send(len(daten).to_bytes(4, 'big'))  
    sock.sendall(daten)             
    sock.close()
    print("Bild gesendet!")


print("Was willst du senden?")
print("1 = Textnachricht")
print("2 = Bilddatei")
wahl = input("Deine Wahl: ").strip()

if wahl == "1":
    text = input("Gib deine Nachricht ein: ")
    sende_nachricht(text)

elif wahl == "2":
    pfad = input("Pfad zum Bild (z. B. ./bild.jpg): ")
    sende_bild(pfad)

else:
    print("Ungültige Eingabe. Bitte 1 oder 2 eingeben.")
