import numpy as np

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

pin = np.array([[1816, 1930, 1802, 1692], [1577, 1632, 1738, 1678]])
pout = np.array([[30, 34, 34, 30], [41, 41, 35, 35]])

H = get_homography_matrix(pin, pout)

print("Homography matrix:")
print(H)

# Test with a new point
test_in = np.array([1798, 1664, 1]).T
test_out = np.matmul(H, test_in)
test_out /= test_out[2]
print("Mapped point:", test_out[:2])
