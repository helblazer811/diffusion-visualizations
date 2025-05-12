import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Generate data for the line
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a set of line segments
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Create a continuous norm to map from data points to colors
norm = plt.Normalize(x.min(), x.max())
lc = LineCollection(segments, cmap='viridis', norm=norm)
lc.set_array(x)
lc.set_linewidth(2)

# Create the plot
fig, ax = plt.subplots()
line = ax.add_collection(lc)
fig.colorbar(line, ax=ax)

# Set the x and y axis limits
ax.set_xlim(x.min(), x.max())
ax.set_ylim(y.min(), y.max())

# Add labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Line Plot with Gradient')

plt.show()