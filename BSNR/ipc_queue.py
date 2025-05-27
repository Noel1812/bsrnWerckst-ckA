
# ipc_queue.py
import queue

class IPC:
    def __init__(self):
        self.to_network = queue.Queue()
        self.from_network = queue.Queue()
