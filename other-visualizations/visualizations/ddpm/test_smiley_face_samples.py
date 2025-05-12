from distributions import make_smiley_face_distribution
import matplotlib.pyplot as plt

# Load the smiley face distribution 
samples = make_smiley_face_distribution(num_samples=100)
# Plot 
plt.scatter(samples[:, 0], samples[:, 1])
plt.show()