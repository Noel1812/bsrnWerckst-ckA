import sys

try:
    print("Starte discovery...")
    from discovery import start_discovery

    if __name__ == "__main__":
        start_discovery()
except Exception as e:
    print("Fehler:", e)
    sys.exit(1)