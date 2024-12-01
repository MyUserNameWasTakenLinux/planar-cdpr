import socket
import math
import time

# Connect to the server
server_address = "127.0.0.1"  # Replace with the server's IP address
port = 65432
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, port))
print("Connected to the server.")
print()

print("Starting Motion")
x_old = 30
y_old = 30
n = 1
try:
    while True:
        # Receive data from the server
        data = client_socket.recv(1024).decode().strip()
        
        if data:
            print(data)
            x_new, y_new = map(float, data.split(","))
            # print(f"Mouse position received: ({x_new}, {y_new})")
            
            # System Motion
            if (math.sqrt((x_new - x_old)**2 + (y_new - y_old)**2) >= 1) and (7 <= x_new <= 53 and 7 <= y_new <= 53):

                print("Movement ",n, "x: ",x_new, "y: ", y_new)  
                # Moving Only if the difference in position is >= 1 and the coordinates within bounds
                # system.update_target_using_coords((x_new, y_new))
                # system.update_command_buffer()
                # system.move_ee_vs()

                x_old = x_new
                y_old = y_new

except KeyboardInterrupt:
    print("Closing connection...")

finally:
    client_socket.close()
    print("Finished Following Target")
