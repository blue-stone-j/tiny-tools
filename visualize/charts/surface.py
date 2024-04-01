'''
Load data.csv to get (x,y,value) and draw them on a 3D surface. If there are some invalid value, you can use mask.csv to 
remove them from graphs. This mask should contain 0 and 1, where 1 means valid and 0 means invalid.
'''

import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Load your CSV data
# csv_data = pd.read_csv('/home/jpw/bag/points_per_voxel2.csv')
# csv_data = pd.read_csv('/home/jpw/bag/height_grad.csv')
# csv_data = pd.read_csv('/home/jpw/bag/zvariance.csv')
csv_data = pd.read_csv('/home/jpw/bag/normalz.csv')
# csv_data = pd.read_csv('/home/jpw/bag/height.csv')
# csv_data = pd.read_csv('/home/jpw/bag/resdiual.csv')
mask_data = pd.read_csv('/home/jpw/bag/mask.csv')  # 加载掩码文件


# Assuming your CSV data is loaded into a DataFrame and is suitable for direct plotting
# Convert the DataFrame to a numpy array if necessary
data = csv_data.values

# 将无效数据点设为np.nan
data[mask_data == 0] = np.nan

# Create meshgrid
x = np.arange(data.shape[1])  # Assuming x coordinates are columns
y = np.arange(data.shape[0])  # Assuming y coordinates are rows
X, Y = np.meshgrid(x, y)


# Create a custom colormap
colors = [(0, 1, 0), (1, 1, 0), (1, 0, 0)]  # R -> G -> B
n_bins = [3]  # Discretizes the interpolation into bins
cmap_name = 'my_list'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
ax.plot_surface(X, Y, data, cmap=cm)

# Labels and title
ax.set_title('3D Surface Plot from CSV Data')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Height (Value)')

plt.show()