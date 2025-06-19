#cli.py
import threading

class ChatCLI:
    def __init__(self, ipc, config):
        self.ipc = ipc
        self.config = config
        self.running = True
    def start(self):
        listener = threading.Thread(target=self.listen_incoming, daemon=True)
        listener.start()
        self.input_loop()

    def input_loop(self):
        print("Willkommen im CLI-Chat! Tippe HELP für Hilfe.")
        while self.running:
            try:
                user_input = input("> ").strip()
                if not user_input:
                    continue

                command, *args = user_input.split(maxsplit=1)
                cmd = command.upper()

                if cmd == "HELP":
                    self.print_help()
                elif cmd == "JOIN":
                    self.join(args)
                elif cmd == "LEAVE":
                    self.leave()
                elif cmd == "MSG":
                    self.msg(args)
                elif cmd == "WHO":
                    self.who()
                elif cmd == "SET":
                    self.set_config(args)
                elif cmd == "EXIT":
                    print("Beende Chat...")
                    self.running = False
                else:
                    print("Unbekannter Befehl.")
            except KeyboardInterrupt:
                print("\nAbbruch durch Benutzer.")
                self.running = False

    def listen_incoming(self):
        while self.running:
            try:
                msg = self.ipc.from_network.get(timeout=1)
                print(f"\n[Empfangen] {msg}")
            except:
                continue

    def join(self, args):
        if not args:
            print("Syntax: JOIN <Handle>")
            return
        self.config["handle"] = args[0]
        msg = f"JOIN {self.config['handle']} {self.config['port']}"
        self.ipc.to_network.put(msg)
        print(f"Gesendet: {msg}")

    def leave(self):
        msg = f"LEAVE {self.config['handle']}"
        self.ipc.to_network.put(msg)
        print("Chat verlassen.")

    def msg(self, args):
        if not args or len(args[0].split(maxsplit=1)) != 2:
            print("Syntax: MSG <Handle> <Nachricht>")
            return
        recipient, text = args[0].split(maxsplit=1)
        msg = f"MSG {recipient} {text}"
        self.ipc.to_network.put(msg)
        print(f"Nachricht an {recipient} gesendet.")

    def who(self):
        self.ipc.to_network.put("WHO")
        print("WHO-Anfrage gesendet.")

    def set_config(self, args):
        if not args or len(args[0].split(maxsplit=1)) != 2:
            print("Syntax: SET <Parameter> <Wert>")
            return
        param, value = args[0].split(maxsplit=1)
        if param in self.config:
            self.config[param] = value
            print(f"{param} aktualisiert auf {value}")
        else:
            print("Unbekannter Parameter.")

    def print_help(self):
        print("""
Befehle:
  JOIN <Handle>             - Dem Chat beitreten
  LEAVE                     - Chat verlassen
  MSG <Handle> <Text>       - Nachricht senden
  WHO                       - Nutzer im Netzwerk suchen
  SET <Param> <Wert>        - Konfiguration ändern
  EXIT                      - Beenden
""")
