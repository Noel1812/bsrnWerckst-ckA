import sys
import tomli
from multiprocessing import Process, Queue
from threading import Thread
from src.cli import cli_loop
from src.network import network_loop
from src.discovery import discovery_loop

def load_config(path):
    with open(path, "rb") as f:
        return tomli.load(f)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main_dynamic.py config/settings1.toml")
        exit(1)

    config_path = sys.argv[1]
    config = load_config(config_path)
    message_queue = Queue()

    cli_thread = Thread(target=cli_loop, args=(message_queue,))
    cli_thread.start()

    net_proc = Process(target=network_loop, args=(message_queue, config_path))
    disc_proc = Process(target=discovery_loop, args=(config_path,))
    net_proc.start()
    disc_proc.start()

    cli_thread.join()
    net_proc.terminate()
    disc_proc.terminate()

