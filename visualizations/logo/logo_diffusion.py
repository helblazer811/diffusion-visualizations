import numpy as np
import pandas as pd
from PIL import Image
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def sample_points_in_mask(mask, num_points):
    # Find all the indices where the mask is True
    mask_indices = np.argwhere(mask)
    # Randomly choose indices from the list of mask indices
    chosen_indices = mask_indices[np.random.choice(len(mask_indices), num_points, replace=False)]
    # Add noise to the chosen indices to sample points between cells
    noise = np.random.uniform(-0.5, 0.5, size=(num_points, 2))
    interpolated_points = chosen_indices + noise
    
    return interpolated_points

def compute_linear_noise_schedule(min, max, num):
    return np.linspace(min, max, num)

def compute_cosine_noise_schedule(start, end, num, tau=1, clip_min=1e-9):
    # A gamma function based on cosine function.
    def cosine_schedule(t):
        v_start = math.cos(start * math.pi / 2) ** (2 * tau)
        v_end = math.cos(end * math.pi / 2) ** (2 * tau)
        output = math.cos((t * (end - start) + start) * math.pi / 2) ** (2 * tau)
        output = (v_end - output) / (v_end - v_start)
        return np.clip(output, clip_min, 1.0)
    # Linearly sample timesteps
    timesteps = np.linspace(0, 1, num)
    return np.array([cosine_schedule(t) for t in timesteps])

def add_noise(x_init, time):
    """
        Here we are going to add noise to given x_init 

        Args: 
            x_init: np.array of shape (N, 2)
            time: int, the time step
    """
    T = 1000
    betas = compute_linear_noise_schedule(1e-4, 1e-3, T)
    # print(betas[:10])
    # betas = compute_cosine_noise_schedule(0, 1, 1000)
    alphas = 1 - betas
    # Sample standard gaussian noise
    noise = np.random.randn(*x_init.shape)
    # Compute variance
    standard_deviation = (1 - np.prod(alphas[:time])) ** 0.5 # From the DDPM paper, the variance is one minus the product of the alphas up to t
    assert np.all(np.prod(alphas[:time]) >= 0), np.prod(alphas[:time])
    assert not np.isnan(np.prod(alphas[:time]) ** 0.5)
    mean = np.prod(alphas[:time]) ** 0.5 * x_init
    # Ensure none are nan
    assert not np.isnan(standard_deviation)
    assert not np.isnan(mean).any()

    return mean + standard_deviation * noise

def make_scatter_plot_animation():
    # Generate random data points
    np.random.seed(0)
    n_points = 100
    x_data = np.random.rand(n_points)
    y_data = np.random.rand(n_points)
    z_data = np.random.rand(n_points) * 100  # Color data

    fig, ax = plt.subplots()
    sc = ax.scatter(x_data, y_data, c=z_data, cmap='viridis', s=100, alpha=0.6)

    def update(frame):
        # Update data points
        x_data = np.random.rand(n_points)
        y_data = np.random.rand(n_points)
        z_data = np.random.rand(n_points) * 100
        # Update scatter plot
        sc.set_offsets(np.column_stack((x_data, y_data)))
        sc.set_array(z_data)
        
        return sc,

    # Create animation
    ani = FuncAnimation(fig, update, frames=range(100), interval=200)
    # Save the animation as a video file
    ani.save('scatter_animation.mp4', writer='ffmpeg')

    plt.show()

if __name__ == "__main__":
    # Import the mask image
    image = Image.open("mask.png").convert("L")
    # Convert it to a binary mask
    mask = 1 - (np.array(image) > 128).astype(np.float32)
    # Flip horizontally and transpose
    mask = np.flip(mask, axis=0).T
    # Sample points uniformly in the mask
    num_points = 8000
    noise_free_data = sample_points_in_mask(mask, num_points)
    # Rescale the points to be between -4 and 4
    noise_free_data = (noise_free_data - noise_free_data.min(axis=0)) / (noise_free_data.max(axis=0) - noise_free_data.min(axis=0)) * 6 - 3
    # Create a pandas data frame containing samples of the spiral function data over different time scales
    for time in range(0, 1000):
        noisy_data = add_noise(noise_free_data, time)
        # CLip to a range of -3 to 3
        noisy_data = np.clip(noisy_data, -4, 4)
        # Add the time column
        noisy_data = np.append(noisy_data, np.ones((noisy_data.shape[0], 1)) * time, axis=1)
        # Add the noisy data to the data frame
        if time == 0:
            df = pd.DataFrame(noisy_data, columns=['x', 'y', 'time'])
        else:
            df = pd.concat([df, pd.DataFrame(noisy_data, columns=['x', 'y', 'time'])], axis=0)

    fig, ax = plt.subplots(figsize=(15, 3))
    sc = ax.scatter(
        df.loc[df['time'] == 999, 'x'], 
        df.loc[df['time'] == 999, 'y'],
        cmap='viridis', 
        s=5, 
        alpha=0.8,
        edgecolors='none'
    )
    # set x and y limits
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)

    def update(frame):
        # Update data points
        x_data = df.loc[df['time'] == 1000 - frame, 'x']
        y_data = df.loc[df['time'] == 1000 - frame, 'y']
        # Update scatter plot
        sc.set_offsets(np.column_stack((x_data, y_data)))
        
        return sc,

    # Create animation
    ani = FuncAnimation(fig, update, frames=range(1000), interval=100)
    # Reverse the animation 
    # Save the animation as a video file
    ani.save('scatter_animation.mp4', writer='ffmpeg', dpi=500)
    # Convert the video to a gif
