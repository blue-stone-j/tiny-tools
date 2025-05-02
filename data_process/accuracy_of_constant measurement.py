"""
# This script analyzes a CSV file containing measurement data, computes the mean, standard deviation,
# and range of the measurements, and visualizes the results. It also computes the smallest enclosing circle
# for the 2D points and finds a circle that covers 90% of the points, useful for handling sparse outliers.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import miniball

# Load the CSV file
df = pd.read_csv("../data/csv_json.csv", sep='\s+', engine='python')

# Extract 2nd and 3rd columns (1-based index -> 1 and 2)
X = df.iloc[:, 1].values
Y = df.iloc[:, 2].values

### calculate mean, standard deviation and range
def analyze_measurement(data, name, true_value=None):
    mean_val = np.mean(data)
    std_val = np.std(data)
    min_val = np.min(data)
    max_val = np.max(data)

    print(f"\n{name} Analysis:")
    print(f"  Mean: {mean_val:.5f}")
    print(f"  Std Dev: {std_val:.5f}")
    print(f"  Min: {min_val:.5f}, Max: {max_val:.5f}")
    print(f"  Range: {(max_val - min_val):.5f}")

    if true_value is not None:
        abs_error = np.abs(data - true_value)
        rel_error = abs_error / np.abs(true_value)
        rmse = np.sqrt(np.mean((data - true_value)**2))
        print(f"  RMSE: {rmse:.5f}")
        print(f"  Mean Abs Error: {np.mean(abs_error):.5f}")
        print(f"  Mean Rel Error: {np.mean(rel_error) * 100:.2f}%")

    # Optional: visualize
    fig = plt.figure()
    fig.canvas.manager.set_window_title(f'{name} Over Samples')
    plt.plot(data, label=name)
    plt.axhline(mean_val, color='r', linestyle='--', label='Mean')
    plt.title(f'{name} Over Samples')
    plt.legend()
    plt.grid(True)
    plt.show()

# Analyze both
analyze_measurement(X, 'X')            # Replace with true_value=X_true if known
analyze_measurement(Y, 'Y')            # Replace with true_value=Y_true if known

###############################

### find the smallest closing circle for 2D points

# Form list of 2D points
points = np.column_stack((X, Y))

# Compute the smallest enclosing circle
center, radius_squared = miniball.get_bounding_ball(points)
radius = np.sqrt(radius_squared)

print(f"\nSmallest enclosing circle center: {center}")
print(f"Radius: {radius:.5f}")

# Plot the result
fig, ax = plt.subplots()
fig.canvas.manager.set_window_title('Minimum Enclosing Circle')
ax.scatter(X, Y, label='Points')
circle = plt.Circle(center, radius, color='r', fill=False, label='Enclosing Circle')
ax.add_patch(circle)
ax.plot(center[0], center[1], 'ro', label='Center')
ax.set_aspect('equal', 'box')
plt.title('Minimum Enclosing Circle')
plt.legend()
plt.grid(True)
plt.show()

###############################

### find a smallest closing circle to cover 90% points. It's useful to depress sparse outliers.

def minimum_partial_enclosing_circle(points, ratio=0.9, trials=1000):
    n_points = len(points)
    k = int(np.ceil(n_points * ratio))
    best_radius = np.inf
    best_center = None

    for _ in range(trials):
        subset = points[np.random.choice(n_points, k, replace=False)]
        center, r2 = miniball.get_bounding_ball(subset)
        radius = np.sqrt(r2)
        if radius < best_radius:
            best_radius = radius
            best_center = center

    return best_center, best_radius

# Compute 90% enclosing circle
center, radius = minimum_partial_enclosing_circle(points, ratio=0.9)

print(f"\nPartial enclosing circle center: {center}")
print(f"Radius: {radius:.5f}")

# Plot
fig, ax = plt.subplots()
fig.canvas.manager.set_window_title(f'Minimum Enclosing Circle for 90% of Points')
ax.scatter(X, Y, label="Points")
circle = plt.Circle(center, radius, color='r', fill=False, label='90% Enclosing Circle')
ax.add_patch(circle)
ax.plot(center[0], center[1], 'ro', label='Center')
ax.set_aspect('equal', 'box')
plt.title('Minimum Enclosing Circle for 90% of Points')
plt.legend()
plt.grid(True)
plt.show()