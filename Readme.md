# ICP Algorithm Repository

This repository contains an implementation of the Iterative Closest Point (ICP) algorithm for point cloud registration.

## App Folder

- **main.py:** Main script for running the ICP algorithm.
- **display3d.py:** Script for 3D point cloud visualization using Pangolin.
- **display_with_mlab.py:** Alternative script for 3D point cloud visualization using Matplotlib (mpl_toolkits.mplot3d).
- **utils.py:** Utility functions used in the implementation.

## ICP Algorithm

The Iterative Closest Point (ICP) algorithm is a widely used technique in computer vision and robotics for aligning two or more point clouds. It iteratively minimizes the difference between the source and target point clouds by estimating the rigid transformation (translation and rotation) between them.

## Pangolin Library

The 3D point cloud visualization is achieved using the Pangolin library. It provides a simple interface for interactive 3D graphics rendering.

## Usage

1. Install the required dependencies (`pip install -r requirements.txt`).
2. Run `main.py` to execute the ICP algorithm.
3. Explore 3D visualizations with `display3d.py` or `display_with_mlab.py`.
