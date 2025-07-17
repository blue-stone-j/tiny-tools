import matplotlib.pyplot as plt
from collections import Counter

# Sample list of integer values
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 1, 1, 3]

# Count frequency of each integer
counter = Counter(data)

# Separate keys and counts for plotting
values = sorted(counter.keys())
frequencies = [counter[v] for v in values]

# Plot
plt.bar(values, frequencies)
plt.xlabel('Integer Value')
plt.ylabel('Frequency')
plt.title('Frequency of Integer Values')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.show()
