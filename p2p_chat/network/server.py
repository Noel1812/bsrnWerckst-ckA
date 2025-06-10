import socket

#1 - Server sets up a listening socket
def start_server():
 with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', 65432))
    s.listen()
    print("Server is listening on port 65432...")

    #2 - Server accepts a connection
    conn, addr = s.accept()
    # Accepting a connection from a client
    with conn:
        # Print the address of the connected client
        print(f"Connected by {addr}")

        #3 - Server receives data from the client
        
        while True:
            # Receive data from the client
            data = conn.recv(1024)
            # If no data is received, the connection is closed
            if not data:
                break
            conn.sendall(data)