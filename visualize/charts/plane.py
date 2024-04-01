'''
Load data.csv to get (x,y,value) and draw them on a plane. If there are some invalid value, you can use mask.csv to 
remove them from graphs. This mask should contain 0 and 1, where 1 means valid and 0 means invalid.
'''


import matplotlib.pyplot as plt
import pandas as pd  # Import pandas for reading the CSV
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Read data from CSV file
data_file = pd.read_csv('data.csv')
mask_file = pd.read_csv('mask.csv')


'''
# If you don't use mask
filtered_data = data_file

# if you use mask
filtered_data = np.where(mask_file == 1, data_file, np.nan)
'''

filtered_data = np.where(mask_file == 1, data_file, np.nan)
#filtered_data = data_file

# Create a custom colormap
colors = [(0, 1, 0), (1, 1, 0), (1, 0, 0)]  # R -> G -> B
n_bins = [3]  # Discretizes the interpolation into bins
cmap_name = 'my_list'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

# Create the heatmap
plt.imshow(filtered_data, cmap=cm, interpolation='nearest',origin='lower')
# plt.imshow(filtered_data, cmap='hot', interpolation='nearest')

# Add a color bar which maps values to colors
plt.colorbar()

plt.title("Heatmap of CSV Data on XOY Plane")
plt.xlabel("X Coordinate")  # Adjust these labels as appropriate for your CSV data
plt.ylabel("Y Coordinate")
plt.show()