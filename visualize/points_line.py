'''
Draw a 3D line and a 3D point cloud from a txt file. First row is line, 3 values for direction and 3 values for a point 
on this line. For other rows, one row is a point, x,y and z respectively. All values are seperated by space.
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def read_file(filename):
    with open(filename, 'r') as file:
        # lines = file.readlines()
        lines = [line.strip() for line in file if line.strip()]

    # Parse line information
    line_data = list(map(float, lines[0].strip().split()))
    direction = np.array(line_data[:3])
    point_on_line = np.array(line_data[3:6])

    # Parse points
    points = np.array([list(map(float, line.strip().split())) for line in lines[1:]])

    return direction, point_on_line, points

def plot_line_and_points(direction, point_on_line, points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Calculate line points for plotting
    t_values = np.linspace(-0.5, 0.5, 100)  # Adjust range as needed
    line_points = point_on_line[:, None] + direction[:, None] * t_values

    # Plot the line
    ax.plot(line_points[0], line_points[1], line_points[2], label="Line", color="blue")

    # Plot the point cloud
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], label="Point Cloud", color="red")
    # ax.scatter(points[:, 0], points[:, 1], points[:, 2], label="Point Cloud", color="red", markersize=1)

    # Set axis limits
    xlim=(2.4, 3.9)
    ax.set_xlim(xlim)
    ylim=(-0.1, 1.4)
    ax.set_ylim(ylim)
    zlim=(-0.5, 1)
    ax.set_zlim(zlim)

    # Labels and legend
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.show()

# Usage
filename = '../data/points_line.txt'  # Replace with your filename

direction, point_on_line, points = read_file(filename)
plot_line_and_points(direction, point_on_line, points)