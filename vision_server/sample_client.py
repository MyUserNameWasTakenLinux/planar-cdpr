import socket
import struct

def main():
    server_ip = "127.0.0.1"  
    server_port = 9999   

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_sock.connect((server_ip, server_port))
    print("Connected to server")

    message = "Wlk"
    client_sock.sendall(message.encode())
    print(f"Sent: {message}")

    angles = client_sock.recv(32) # CAREFUL HARDCODED
    if len(angles) != 32:
        print("Error did not receive all the angles")
    
    angles = struct.unpack('ffff', angles);

    for angle in angles:
        print(angle)

    client_sock.close()

if __name__ == "__main__":
    main()
