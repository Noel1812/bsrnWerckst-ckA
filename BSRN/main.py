# main.py
from ipc_queue import IPC
from cli import ChatCLI

if __name__ == "__main__":
    config = {
        "handle": "Alice",
        "port": 5000,  # Wird durch JOIN überschrieben
        "whoisport": 4000,
        "autoreply": "",
        "imagepath": "./images"
    }

    ipc = IPC()
    cli = ChatCLI(ipc, config)
    cli.start()
