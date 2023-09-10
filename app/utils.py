import numpy as np
import matplotlib.pyplot as plt
import sys


def get_correspondence_indices(P, Q):
    """For each point in P find closest one in Q."""
    p_size = P.shape[0]
    q_size = Q.shape[0]
    correspondences = []
    for i in range(p_size):
        p_point = P[i]
        min_dist = sys.maxsize
        chosen_idx = -1
        for j in range(q_size):
            q_point = Q[j]
            dist = np.linalg.norm(q_point - p_point)
            if dist < min_dist:
                min_dist = dist
                chosen_idx = j
        correspondences.append((i, chosen_idx))
    return correspondences

def center_data(data, exclude_indices=[]):
    reduced_data = np.delete(data, exclude_indices, axis=0)
    center = np.array([reduced_data.mean()]).T
    return center, data - center
