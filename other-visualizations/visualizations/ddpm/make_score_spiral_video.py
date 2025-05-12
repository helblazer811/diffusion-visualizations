import torch
from train import DiffusionModel
from distributions import make_spiral_data
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from tqdm import tqdm
import seaborn as sns
from scipy.ndimage import gaussian_filter

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
    # Import the trained DM
    diffusion_model = DiffusionModel()
    diffusion_model.load_state_dict(torch.load('models/spiral_model.pth'))
    # # Load the spiral training data
    data = make_spiral_data(num_examples=10000)
    # Sample the score in linearly spaced intervals in the range of the training data
    x = torch.linspace(-5.5, 5.5, 15)
    y = torch.linspace(-5.5, 5.5, 15)
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
    time = torch.Tensor([980]).long().repeat(xy.shape[0])
    score = diffusion_model.predict_noise(xy, time) * 2
    score = -1 * score * 5 # / torch.norm(score, dim=1).reshape(-1, 1) * torch.log(torch.norm(score, dim=1).reshape(-1, 1)) * 5
    # Plot the scores as a quiver plot
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    # Set bakcground color to black
    fig.patch.set_facecolor('black')
    xy = xy.detach().numpy()
    score = score.detach().numpy()
    # Flip vertically 
    # zz = np.flip(zz, axis=0)
    # ax[0].imshow(zz, cmap='viridis', extent=[-6, 6, -6, 6])
    # Plot a 2d histogram of the data samples
    print(f"Data shape: {data.shape}")
    data = data.detach().numpy()
    # ax[0].hist2d(data[:, 0], data[:, 1], bins=100, cmap='viridis')
    # Plot the pdf
    x = np.linspace(-5.5, 5.5, 20)
    y = np.linspace(-5.5, 5.5, 20)
    xx, yy = np.meshgrid(x, y)
    zz = np.zeros_like(xx)
    for i in tqdm(range(20)):
        for j in range(20):
            zz[i, j] = spiral_distribution_pdf([xx[i, j], yy[i, j]])
    # Flip vertically 
    zz = np.flip(zz, axis=0)
    ax.imshow(zz, cmap='viridis', extent=[-5.5, 5.5, -5.5, 5.5])

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
    ax.quiver(xy[:, 0], xy[:, 1], score[:, 0], score[:, 1], scale=200, headwidth=2, color='white', alpha=0.6)
    ax.set_title('Evaluation of the Score Function\n at Low Time Scale (Approx 0)')
    ax.set_xticks([])
    ax.set_yticks([])
    # Generate samples and intermediates
    samples, intermediate_values = diffusion_model.sample(num_samples=50000, num_timesteps=1000)
    intermediate_values = intermediate_values.detach().numpy()
    # Animate the score function over time
    # fig, ax = plt.subplots(1, 1, figsize=(5, 5))

    def update(frame):
        print(frame)
        frame = 999 - frame
        # Update the score
        x = torch.linspace(-5.5, 5.5, 10)
        y = torch.linspace(-5.5, 5.5, 10)
        xx, yy = torch.meshgrid(x, y)   
        xy = torch.stack([xx, yy], dim=-1).reshape(-1, 2)
        time = torch.Tensor([frame]).long().repeat(xy.shape[0])
        score = diffusion_model.predict_noise(xy, time) * 2
        score = -1 * score * 5
        # Clear the axis
        ax.clear()
        # Plot the pdf
        # Flip vertically
        # Make a heatmap of intermediate examples 
        # Make a 2d histogram with numpy 
        hist2d = np.histogram2d(intermediate_values[:, 999 - frame, 0], intermediate_values[:, 999 - frame, 1], bins=400, range=[[-5.5, 5.5], [-5.5, 5.5]])
        # Apply a gaussian filter
        hist2d = gaussian_filter(hist2d[0], sigma=1)
        # ax.hist2d(intermediate_values[:, 999 - frame, 0], intermediate_values[:, 999 - frame, 1], bins=400, cmap='inferno')
        # Plot with imshow
        ax.imshow(hist2d, cmap='viridis', extent=[-5.5, 5.5, -5.5, 5.5])
        # Seaborn kde plot
        # sns.kdeplot(x=intermediate_values[:, 999 - frame, 0], y=intermediate_values[:, 999 - frame, 1], ax=ax, fill=True, levels=100, palette="inferno")
        # Plot the score function
        xy = xy.detach().numpy()
        score = score.detach().numpy()
        ax.quiver(xy[:, 0], xy[:, 1], score[:, 0], score[:, 1], scale=200, headwidth=2, color='white', alpha=0.6, linewidth=1.0)
        ax.set_title(f'Evaluating the Score Function at Time: {frame}')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim([-5.5, 5.5])
        ax.set_ylim([-5.5, 5.5])
        return ax,  

    # Create the animation
    ani = FuncAnimation(fig, update, frames=range(1000), interval=20)
    # Reverse the animation

    ani.save('score_over_time.mp4', writer='ffmpeg', dpi=500)