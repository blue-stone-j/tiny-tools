'''
display a file with several rows and several columns with 3D bars
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap

# Load your CSV data
csv_data = pd.read_csv('your_file.csv')
data = csv_data.values

# Create a grid of x, y coordinates
xpos, ypos = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))

xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros_like(xpos)

# Heights of the bars
dz = data.flatten()

# Create a custom colormap
colors = [(0, 0, 0.5), (1, 1, 0), (1, 0, 0)]  # Heavy Blue -> Yellow -> Red
cmap_name = 'custom1'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

# Map dz values to colors from the custom colormap
norm = plt.Normalize(dz.min(), dz.max())
bar_colors = cm(norm(dz))

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the bars
ax.bar3d(xpos, ypos, zpos, 1, 1, dz, color=bar_colors)

# Labels and title
ax.set_title('3D Bar Plot with Custom Colormap')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Height (Value)')

plt.show()
