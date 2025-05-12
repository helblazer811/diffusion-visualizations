import torch
# from train import make_spiral_data, DiffusionModel, make_gaussian_mixture
from train import DiffusionModel
from distributions import make_gaussian_mixture
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from tqdm import tqdm
import seaborn as sns
import pandas as pd

from scipy import ndimage

# Make a pdf of the gaussian mixture
def gaussian_mixture_pdf(x):
    # Define parameters for each Gaussian
    mean1 = np.array([2.2, 1.5])
    covariance1 = np.eye(2) * 0.4 # Identity covariance matrix for isotropic distribution

    mean2 = np.array([-2.5, 2.5])
    covariance2 = np.eye(2) * 0.5

    mean3 = np.array([0, -2])
    covariance3 = np.eye(2) * 0.7
    # Compute the pdf of each Gaussian
    pdf1 = np.exp(-0.5 * (x - mean1).T @ np.linalg.inv(covariance1) @ (x - mean1)) / (2 * np.pi * np.sqrt(np.linalg.det(covariance1)))
    pdf2 = np.exp(-0.5 * (x - mean2).T @ np.linalg.inv(covariance2) @ (x - mean2)) / (2 * np.pi * np.sqrt(np.linalg.det(covariance2)))
    pdf3 = np.exp(-0.5 * (x - mean3).T @ np.linalg.inv(covariance3) @ (x - mean3)) / (2 * np.pi * np.sqrt(np.linalg.det(covariance3)))
    # Return the sum of the pdfs
    return pdf1 + pdf2 + pdf3

if __name__ == "__main__":
    # Import the trained DM
    diffusion_model = DiffusionModel()
    diffusion_model.load_state_dict(torch.load('models/gmm_model.pth'))
    # # Load the spiral training data
    data = make_gaussian_mixture(num_samples=10000)
    # Sample the score in linearly spaced intervals in the range of the training data
    # x = torch.linspace(-5.5, 5.5, 15)
    # y = torch.linspace(-5.5, 5.5, 15)
    # xx, yy = torch.meshgrid(x, y)
    # xy = torch.stack([xx, yy], dim=-1).reshape(-1, 2)
    # Filter out any coordinates not in a circle of radius 2.8
    # xy = xy[torch.sqrt(xy[:, 0] ** 2 + xy[:, 1] ** 2) <= 3]
    # Sample locations uniformly 
    # Flip vertically
    # xy = xy.flip(1)
    # xy = xy.flip(0)
    # xy = xy.flip(1)
    # Sample the score
    # # Choose a time near 0 in range [0, 1000]
    # time = torch.Tensor([980]).long().repeat(xy.shape[0])
    # score = diffusion_model.predict_noise(xy, time) * 2
    # score = -1 * score * 5 # / torch.norm(score, dim=1).reshape(-1, 1) * torch.log(torch.norm(score, dim=1).reshape(-1, 1)) * 5
    # Plot the scores as a quiver plot
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    # Set bakcground color to black
    fig.patch.set_facecolor('black')
    # xy = xy.detach().numpy()
    # score = score.detach().numpy()
    # Flip vertically 
    # zz = np.flip(zz, axis=0)
    # ax[0].imshow(zz, cmap='viridis', extent=[-6, 6, -6, 6])
    # Plot a 2d histogram of the data samples
    print(f"Data shape: {data.shape}")
    data = data.detach().numpy()
    # ax[0].hist2d(data[:, 0], data[:, 1], bins=100, cmap='viridis')
    # Plot the pdf
    # x = np.linspace(-5.5, 5.5, 400)
    # y = np.linspace(-5.5, 5.5, 400)
    # xx, yy = np.meshgrid(x, y)
    # zz = np.zeros_like(xx)
    # for i in tqdm(range(400)):
    #     for j in range(400):
    #         zz[i, j] = gaussian_mixture_pdf([xx[i, j], yy[i, j]])
    # # Flip vertically 
    # zz = np.flip(zz, axis=0)
    # ax.imshow(zz, cmap='viridis', extent=[-5.5, 5.5, -5.5, 5.5])

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
    # ax.quiver(xy[:, 0], xy[:, 1], score[:, 0], score[:, 1], scale=200, headwidth=2, color='white', alpha=0.6)
    # ax.set_title('Evaluation of the Score Function\n at Low Time Scale (Approx 0)')
    # ax.set_xticks([])
    # ax.set_yticks([])
    # Generate samples and intermediates
    samples, intermediate_values = diffusion_model.sample(num_samples=500000, num_timesteps=1000)
    intermediate_values = intermediate_values.detach().numpy()
    # Animate the score function over time
    # fig, ax = plt.subplots(1, 1, figsize=(5, 5))

    def update(frame):
        print(frame)
        frame = 999 - frame
        # Update the score
        x = torch.linspace(-2.8, 2.8, 7)
        y = torch.linspace(-2.8, 2.8, 7)
        xx, yy = torch.meshgrid(x, y)   
        xy = torch.stack([xx, yy], dim=-1).reshape(-1, 2)
        time = torch.Tensor([frame]).long().repeat(xy.shape[0])
        score = diffusion_model.predict_noise(xy, time) * 2
        score = -1 * score * 5
        xy = xy.detach().numpy()
        score = score.detach().numpy()
        # Clear the axis
        ax.clear()
        # Plot the pdf
        # Flip vertically
        # Make a heatmap of intermediate examples 
        # Make hisotgram with numpy
        hist2d, _, _ = np.histogram2d(intermediate_values[:, 999 - frame, 0], intermediate_values[:, 999 - frame, 1], bins=800, range=[[-2.8, 2.8], [-2.8, 2.8]])
        # Apply a gaussian filter
        hist2d = ndimage.gaussian_filter(hist2d, sigma=3)
        # Average pool
        hist2d = hist2d[::8, ::8]
        # Transpose 
        hist2d = hist2d.T
        # Flip vertically
        hist2d = np.flip(hist2d, axis=0)
        # Apply a gaussian filter
        print(f"Shape of histogram: {hist2d.shape}")
        ax.imshow(hist2d, cmap='inferno', extent=[-2.8, 2.8, -2.8, 2.8])
        # ax.hist2d(intermediate_values[:, 999 - frame, 0], intermediate_values[:, 999 - frame, 1], bins=400, cmap='inferno')
        # Seaborn kde plot
        # sns.kdeplot(x=intermediate_values[:, 999 - frame, 0], y=intermediate_values[:, 999 - frame, 1], ax=ax, fill=True, levels=100, palette="inferno")
        ax.set_xlim([-2.8, 2.8])
        ax.set_ylim([-2.8, 2.8])
        # Plot the score function
        ax.quiver(xy[:, 0], xy[:, 1], score[:, 0], score[:, 1], scale=200, headwidth=2, color='white', alpha=0.8, linewidth=1.7)
        # ax.set_title(f'Evaluating the Score Function at Time: {frame}')
        ax.set_xticks([])
        ax.set_yticks([])
        return ax,  

    # Create the animation
    ani = FuncAnimation(fig, update, frames=range(1000), interval=20)
    # Reverse the animation

    ani.save('score_over_time.mp4', writer='ffmpeg', dpi=500)