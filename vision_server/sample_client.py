import socket

# Connect to the server
server_address = "127.0.0.1"  # Replace with the server's IP address
port = 65432
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, port))
print("Connected to the server.")

try:
    while True:
        # Receive data from the server
        data = client_socket.recv(1024).decode().strip()
        if data:
            x, y = map(float, data.split(","))
            print(f"Mouse position received: ({x}, {y})")
except KeyboardInterrupt:
    print("Closing connection...")
finally:
    client_socket.close()
