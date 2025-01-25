import matplotlib.pyplot as plt

def plot_coordinates_with_colors(file_path):
    x_coords = []
    y_coords = []
    colors = []
    
    # Open and read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into columns
            columns = line.strip().split()
            
            # Extract the first column as color, second and third columns as coordinates
            try:
                color = int(columns[0])  # First column (index)
                x = float(columns[1])    # Second column (x-coordinate)
                y = float(columns[2])    # Third column (y-coordinate)
                x_coords.append(x)
                y_coords.append(y)
                colors.append(color)
            except (IndexError, ValueError) as e:
                print(f"Skipping invalid line: {line.strip()} - Error: {e}")
    
    # Plot the coordinates with color
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(x_coords, y_coords, c=colors, cmap='viridis', marker='o')
    plt.colorbar(scatter, label="Index (Color)")
    plt.title('Coordinates Plot with Colors')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

# Replace 'coordinates.txt' with the path to your file
file_path = '../data/2d_plot.txt'
plot_coordinates_with_colors(file_path)
