from Display3d import Display3D
from math import cos, sin, pi
import numpy as np
from utils import get_correspondence_indices, center_data, compute_cross_covariance

if __name__ == '__main__':
    import time

    d = Display3D()
    angle = pi / 4
    t_true = np.array([[-2], [5], [0]])  # Replace with your desired translation vector

    # Create a 3D rotation matrix with no effect on the Z-axis
    R_true = np.array([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1]  # This row keeps the Z-axis unchanged
    ])

    num_points = 30
    true_data = np.zeros((3, num_points))
    true_data[0, :] = range(0, num_points)
    true_data[1, :] = 0.2 * true_data[0, :] * np.sin(0.5 * true_data[0, :])
    # Move the data
    moved_data = R_true.dot(true_data) + t_true

    # Assign to variables we use in formulas.
    Q = true_data.T
    P = moved_data.T

    color_Q = np.zeros_like(Q)
    color_P = np.zeros_like(P)
    color_Q[:] = [1, 0, 0]
    color_P[:] = [0, 1, 0]

    center_Q, Q_centered = center_data(Q)
    P_copy = P.copy()
    iterations = 10
    exclude_indices = []
    for i in range(iterations):
        center_P, P_centered = center_data(P_copy, exclude_indices=exclude_indices)
        correspondences = get_correspondence_indices(P_centered, Q_centered)
        # print(correspondences)
        cov, exclude_indices = compute_cross_covariance(P_centered, Q_centered, correspondences)
        # print(cov)
        U, S, V_T = np.linalg.svd(cov)
        R_found = U.dot(V_T)
        print("R_found =\n", R_found,R_found.shape)
        t_found = center_Q - np.dot(center_P, R_found.T)
        print("t_found =\n", t_found,t_found.shape)
        P_copy = np.dot(P_copy, R_found.T) + t_found.T

        d.paint([Q, P_copy], [color_Q, color_P])
        time.sleep(1)
