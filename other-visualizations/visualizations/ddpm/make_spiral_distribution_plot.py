from train import make_spiral_data
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def spiral_distribution_pdf(location, num_gaussians=1000, std=0.3, rescale_factor=0.3):
    """
        This is the probability density function of the spiral distribution
    """
    # Add up a bunch of gaussians centered along points on a spiral
    total_gaussian_pdf = 0.0
    angles = np.linspace(0, 4 * np.pi, num_gaussians)
    for i in range(num_gaussians):
        # Compute the location of the gaussian
        angle = angles[i]
        x = rescale_factor * angle * np.cos(angle)
        y = rescale_factor * angle * np.sin(angle)
        # Compute the pdf
        pdf = np.exp(-((location[0] - x) ** 2 + (location[1] - y) ** 2) / (2 * std ** 2))
        total_gaussian_pdf += pdf
        
    return total_gaussian_pdf

if __name__ == "__main__":
    # Create an inferno meshgrid and do imshow
    x = np.linspace(-3.75, 4.5, 200)
    y = np.linspace(-4, 3.5, 200)
    xx, yy = np.meshgrid(x, y)
    zz = np.zeros_like(xx)
    for i in tqdm(range(200)):
        for j in range(200):
            zz[i, j] = 2 * spiral_distribution_pdf([xx[i, j], yy[i, j]])
    
    plt.imshow(zz, cmap='inferno')
    plt.show()
