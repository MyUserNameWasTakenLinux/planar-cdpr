import math
from Matrix import *

# Calculates the determinant of a 2x2 matrix
def det(A):
    return (A.elems[0][0] * A.elems[1][1]) - (A.elems[0][1] * A.elems[1][0])

def newton_pos_to_angle(p : Mat, theta_guess : Mat):
    theta_old = theta_guess # Our inital guess
    L1 = 10.4 # Length on the first link (Basically, L2 from the Main)
    L2 = 10.5 # Length of the second link (Basically, L3 from the Main)

    for i in range(10):
        t1 = theta_old.elems[0][0] # joint angle 1
        t2 = theta_old.elems[1][0] # joint angle 2
        J = Mat([[-L1 * math.sin(t1) - L2 * math.sin(t1 + t2), -L2 * math.sin(t1 + t2)],
             [L1 * math.cos(t1) + L2 * math.cos(t1 + t2), L2 * math.cos(t1 + t2)]]) # The jacobian
        J_inv = Mat([
            [J.elems[1][1] / det(J), -J.elems[0][1] / det(J)],
            [-J.elems[1][0] / det(J), J.elems[0][0] / det(J)]
        ]) # The inverse of the jacobian
        F = Mat([
            [L1 * math.cos(t1) + L2 * math.cos(t1 + t2) - p.elems[0][0]],
            [L1 * math.sin(t1) + L2 * math.sin(t1 + t2) - p.elems[1][0]]
        ]) # The forward kinematic equation
        theta_old = theta_old - (J_inv * F) # Iteration
    
    return theta_old

# Midpoint of 2 dim vectors
def midpoint(v : Mat, w : Mat):
    return Mat([
        [(v.elems[0][0] + w.elems[0][0]) / 2],
        [(v.elems[1][0] + w.elems[1][0]) / 2]
    ])
