import torch
from train import make_spiral_data, DiffusionModel

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


def spiral_distribution_pdf(location, num_gaussians=1000, std=0.25):
    """
        This is the probability density function of the spiral distribution
    """
    # Add up a bunch of gaussians centered along points on a spiral
    total_gaussian_pdf = 0.0
    angles = np.linspace(0, 4 * np.pi, num_gaussians)
    for i in range(num_gaussians):
        # Compute the location of the gaussian
        angle = angles[i]
        x = 0.3 * angle * np.cos(angle)
        y = 0.3 * angle * np.sin(angle)
        # Compute the pdf
        pdf = np.exp(-((location[0] - x) ** 2 + (location[1] - y) ** 2) / (2 * std ** 2))
        total_gaussian_pdf += pdf
        
    return total_gaussian_pdf

if __name__ == "__main__":
    # Import the trained DM
    diffusion_model = DiffusionModel()
    diffusion_model.load_state_dict(torch.load('models/spiral_model.pth'))
    # # Load the spiral training data
    spiral_data = make_spiral_data(num_examples=1000, std=0.0, rescale_factor=0.3)
    # Sample the score in linearly spaced intervals in the range of the training data
    x = torch.linspace(-3.25, 3.9, 15)
    y = torch.linspace(-3.75, 3.25, 15)
    xx, yy = torch.meshgrid(x, y)
    xy = torch.stack([xx, yy], dim=-1).reshape(-1, 2)
    # Filter out any coordinates not in a circle of radius 3.5
    # xy = xy[torch.sqrt(xy[:, 0] ** 2 + xy[:, 1] ** 2) <= 3]
    # Sample locations uniformly 
    # Flip vertically
    # xy = xy.flip(1)
    # xy = xy.flip(0)
    # xy = xy.flip(1)
    # Sample the score
    # Choose a time near 0 in range [0, 1000]
    time = torch.Tensor([20]).long().repeat(xy.shape[0])
    score = diffusion_model.predict_noise(xy, time) * 2
    score = -1 * score / torch.norm(score, dim=1).reshape(-1, 1) * torch.log(torch.norm(score, dim=1).reshape(-1, 1)) * 5
    # Plot the scores as a quiver plot
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    xy = xy.detach().numpy()
    score = score.detach().numpy()
    # Plot a heatmap of the data likelihood
    x = np.linspace(-3.25, 3.9, 200)
    y = np.linspace(-3.75, 3.25, 200)
    xx, yy = np.meshgrid(x, y)
    zz = np.zeros_like(xx)
    for i in tqdm(range(200)):
        for j in range(200):
            zz[i, j] = spiral_distribution_pdf([xx[i, j], yy[i, j]])

    # Flip vertically 
    zz = np.flip(zz, axis=0)
    ax[0].imshow(zz, cmap='viridis', extent=[-3.25, 3.9, -3.75, 3.25])
    # Here we will draw N samples, then take intermediate values at a late time scale 
    # and then cmpute the score function at that time scale
    # _, intermediate_samples = diffusion_model.sample(100)
    # # Take the samples at a time scale of 50
    # intermediate_samples = intermediate_samples[:, -50, :]
    # print(f"Intermediate samples shape: {intermediate_samples.shape}")
    # # Compute the score at this time scale for the samples
    # score = diffusion_model.predict_noise(intermediate_samples, torch.Tensor([50]).long().repeat(intermediate_samples.shape[0]))
    # score *= 5
    # Plot samples of the dsitribution
    # ax[0].scatter(spiral_data[:, 0], spiral_data[:, 1], s=5, color='black')
    # intermediate_samples = intermediate_samples.detach().numpy() 
    # score = score.detach().numpy() 
    ax[0].quiver(xy[:, 0], xy[:, 1], score[:, 0], score[:, 1], scale=200, headwidth=2, color='white')
    ax[0].set_title('Evaluation of the Score Function\n at Low Time Scale (Approx 0)')
    ax[0].set_xticks([])
    ax[0].set_yticks([])

    plt.savefig('plots/score_plot.png', dpi=300)