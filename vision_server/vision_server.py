import numpy as np
import cv2
import time
import socket


current_mouse_pos = [0, 0]
pos_changed = False

def get_homography_matrix(input_points, output_points):
    """
    Given points from the image frame and the real world frame compute
    the homography matrix H

    Arguments:
    input_points: A 2xN np.array of input points
    output_points: A 2xN np.array of output points

    Returns:
    A 3x3 homography matrix
    """

    input_points = input_points.transpose()
    output_points = output_points.transpose()

    if input_points.shape != output_points.shape:
        raise ValueError("Input points and output points do not match dimensions")
    if input_points.shape[1] != 2:
        raise ValueError("Incorrect format, make sure points form columns")
    
    n = input_points.shape[0]
    if n < 4:
        raise ValueError("Need at least 4 points to compute the homography matrix")
    
    A = []
    for i in range(n):
        X, Y = input_points[i]
        x, y = output_points[i]
        A.append([-X, -Y, -1, 0, 0, 0, x * X, x * Y, x])
        A.append([0, 0, 0, -X, -Y, -1, y * X, y * Y, y])
    
    A = np.array(A)

    _, _, Vt = np.linalg.svd(A)
    H = Vt[-1].reshape((3, 3))

    return H

def get_pixel_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse clicked at position: ({x}, {y})")
        if param[0] < 4:
            (param[1])[0, param[0]] = x
            (param[1])[1, param[0]] = y
            param[0] += 1
        else:
            global current_mouse_pos
            global pos_changed
            pos_changed = True
            current_mouse_pos[0] = x
            current_mouse_pos[1] = y



# Set up the TCP server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 65432))  # Bind to all interfaces on port 65432
server_socket.listen(1)
print("Waiting for a connection...")

# Wait for a client to connect
conn, addr = server_socket.accept()
print(f"Connected by {addr}")


video_capture = cv2.VideoCapture(2)
success, frame = video_capture.read()

# Index, pin, pout
calibration = [0, np.zeros(shape=(2, 4)), np.array([[30, 34, 34, 30], [41, 41, 35, 35]])]

H = None

while success:
    cv2.imshow("Frame", cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    cv2.setMouseCallback("Frame", get_pixel_position, calibration)

    if calibration[0] == 4:
        H = get_homography_matrix(calibration[1], calibration[2])
        calibration[0] = 5
    
    if calibration[0] == 5 and pos_changed:
        point = np.array([[current_mouse_pos[0]], [current_mouse_pos[1]], [1]])
        point = np.matmul(H, point)
        point = point[:2] / point[2]
        print("Point: ", point)
        conn.sendall(f"{point[0, 0]}, {point[1, 0]}\n".encode())
        pos_changed = False

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Exiting")
        break

    success, frame = video_capture.read()

# H = get_homography_matrix(calibration[1], calibration[2])


conn.close()
server_socket.close()

cv2.destroyAllWindows()