from Display3d import Display3D
from math import cos, sin, pi
import numpy as np
from utils import get_correspondence_indices, center_data

if __name__ == '__main__':
    import time

    d = Display3D()
    angle = pi / 4
    t_true = np.array([[-2], [5], [0]])  # Replace with your desired translation vector

    # Create a 3D rotation matrix with no effect on the Z-axis
    R_true = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]  # This row keeps the Z-axis unchanged
    ])
    # Generate data as a list of 2d points
    num_points = 30
    true_data = np.zeros((3, num_points))
    true_data[0, :] = range(0, num_points)
    true_data[1, :] = 0.2 * true_data[0, :] * np.sin(0.5 * true_data[0, :])
    # Move the data
    moved_data = R_true.dot(true_data) + t_true

    # Assign to variables we use in formulas.
    Q = true_data.T
    P = moved_data.T
    while 1:
        color_Q = np.zeros_like(Q)
        color_P = np.zeros_like(P)
        color_Q[:] = [1, 0, 0]
        color_P[:] = [0, 1, 0]
        center_Q, Q_centered = center_data(Q)
        center_P, P_centered = center_data(P)
        correspondences = get_correspondence_indices(P_centered, Q_centered)
        print(correspondences)
        d.paint([Q_centered, P_centered], [color_Q, color_P])
        time.sleep(1)
