'''
display a file with several rows and several columns with smooth surface
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

# Load your CSV data
csv_data = pd.read_csv('your_file.csv')
data = csv_data.values

# Original grid
x = np.arange(data.shape[1])
y = np.arange(data.shape[0])
X, Y = np.meshgrid(x, y)
Z = data

# Create a denser grid for interpolation
x2 = np.linspace(x.min(), x.max(), 300)  # Increase 300 to make it even smoother
y2 = np.linspace(y.min(), y.max(), 300)
X2, Y2 = np.meshgrid(x2, y2)

# Interpolate using griddata
Z2 = griddata((X.flatten(), Y.flatten()), Z.flatten(), (X2, Y2), method='cubic')

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface with interpolated data
ax.plot_surface(X2, Y2, Z2, cmap='hot', edgecolor='none')

# Labels and title
ax.set_title('Smooth 3D Surface Plot from CSV Data')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Height (Value)')

plt.show()
