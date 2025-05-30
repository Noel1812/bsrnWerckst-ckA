def cli_loop(queue):
    print("Willkommen im P2P-Chat (CLI). Tippe /help für Befehle.")
    while True:
        user_input = input(">> ").strip()

        if user_input.startswith("/send"):
            try:
                _, target, message = user_input.split(" ", 2)
                queue.put((target, message))
            except ValueError:
                print("⚠️  Syntax: /send <ip:port> <nachricht>")

        elif user_input == "/exit":
            print("Chat wird beendet.")
            break

        elif user_input == "/help":
            print("Verfügbare Befehle:\n  /send <ip:port> <msg>\n  /exit\n  /help")

        else:
            print("⚠️  Unbekannter Befehl. Tippe /help.")