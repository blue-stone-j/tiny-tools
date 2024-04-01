'''
Load data.csv to get (x,y,value) and draw them on a 3D surface. Linear interpolate is used to make surface smooth. 
If there are some invalid value, you can use mask.csv to remove them from graphs. This mask should contain 0 and 1, 
where 1 means valid and 0 means invalid.
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from matplotlib.colors import LinearSegmentedColormap

# Load your CSV data
csv_data = pd.read_csv('data.csv')
mask_data = pd.read_csv('mask.csv')  # 加载掩码文件

data = csv_data.values

# 将无效数据点设为np.nan
data[mask_data == 0] = np.nan

# Original grid
x = np.arange(data.shape[1])
y = np.arange(data.shape[0])
X, Y = np.meshgrid(x, y)
Z = data

# Create a denser grid for interpolation
x2 = np.linspace(x.min(), x.max(), 300)
y2 = np.linspace(y.min(), y.max(), 300)
X2, Y2 = np.meshgrid(x2, y2)

# Interpolate using griddata, ignoring np.nan by using 'valid' mask
valid_mask = ~np.isnan(Z)
Z2 = griddata((X[valid_mask], Y[valid_mask]), Z[valid_mask], (X2, Y2), method='cubic')

# Create a custom colormap
colors = [(0, 1, 0), (1, 1, 0), (1, 0, 0)]  # R -> G -> B
cmap_name = 'my_list'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface with interpolated data
ax.plot_surface(X2, Y2, Z2, cmap=cm, edgecolor='none')

# Labels and title
ax.set_title('Smooth 3D Surface Plot with Custom Colormap')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Height (Value)')

plt.show()
