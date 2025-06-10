import socket
from config.loader import load_config # Import the load_config function from the config.loader module

def start_client():
    config = load_config()  # Load configuration from the default path
    peer = config["peers"][0] # Assuming the first peer is the one we want to connect to
    host, port = peer.split(":") # Split the peer address into host and port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Create a TCP socket
        s.connect((host, int(port))) # Connect to the peer
        s.sendall(b'Hello, Server!') # Send a message to the server
        data = s.recv(1024) # Receive a response from the server
        print(f"Received from server: {data.decode()}") # Print the response from the server

if __name__ == "__main__": # This ensures the script runs only when executed directly
    start_client() # Start the client
