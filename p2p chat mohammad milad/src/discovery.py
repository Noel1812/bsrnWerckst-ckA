import socket

def is_udp_port_available(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("0.0.0.0", port))
        s.close()
        return True
    except:
        return False

def discovery_loop(config_path):
    import tomli
    with open(config_path, "rb") as f:
        config = tomli.load(f)
    whoisport = config["whoisport"]

    if not is_udp_port_available(whoisport):
        print(f"❌ Discovery-Port {whoisport} ist bereits belegt.")
        return

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("0.0.0.0", whoisport))
    print("[DISCOVERY] Dienst gestartet.")

    while True:
        data, addr = s.recvfrom(1024)
        if data == b"WHOIS":
            response = f'{config["handle"]}|127.0.0.1|{config["port"]}'.encode()
            s.sendto(response, addr)
