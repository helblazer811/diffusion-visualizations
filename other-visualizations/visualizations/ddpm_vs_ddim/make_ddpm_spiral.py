from matplotlib.collections import LineCollection
from train import DDPMDiffusionModel
from distributions import make_spiral_data
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import torch
import seaborn as sns
import pandas as pd

if __name__ == "__main__":
    # Load the diffusion model
    diffusion_model = DDPMDiffusionModel()
    diffusion_model.load_state_dict(torch.load('models/spiral_model.pth'))
    # Load the data
    spiral_data = make_spiral_data(num_examples=500, std=0.05, rescale_factor=0.3)
    # Show generation of samples from it using the trained diffusion model
    # Black background figure
    plt.figure(figsize=(5, 5))
    plt.ylim(-4, 4)
    plt.xlim(-4, 4.5)
    # Plot the spiral data
    spiral_data = spiral_data.detach().numpy()
    # Show the plot
    plt.legend()
    # Show the path of each of the samples moving over time
    # Generate N samples from the model, and save the intermediate paths
    num_samples = 1
    num_inference_steps = 50
    plot_every_n_steps = 1
    samples, intermediate_values = diffusion_model.sample(num_samples=num_samples, num_timesteps=num_inference_steps)
    # Intermediate values has shape (num_samples, num_inference_steps, 2)
    # Pull out only every 50 samples
    intermediate_values = intermediate_values[:, ::plot_every_n_steps, :]
    # Now plot the intermediate values
    def animate(i):
        if i == 0:
            return
        sample_index = i // (num_inference_steps // plot_every_n_steps)
        print(sample_index)
        intermediate_index = i % (num_inference_steps // plot_every_n_steps)
        # Plot a line graph of the samples from sample_start_index to interemdiate_index
        plt.clf()
        plt.ylim(-4, 4)
        plt.xlim(-4, 4.5)
        plt.axis('off')
        plt.scatter(spiral_data[:, 0], spiral_data[:, 1], alpha=0.4, color="#67a9cf", label="Ground Truth Data")
        # Plot a line plot for the intermediate values of the sample index up until this point
        # Create a continuous norm to map from data points to colors
        for sample_index in range(num_samples):
            for intermediate_index in range(intermediate_values.shape[1]):
                prev = intermediate_values[sample_index][:intermediate_index]
                next = intermediate_values[sample_index][:intermediate_index, 1]
                alpha = intermediate_index / intermediate_values.shape[1]
                plt.plot(
                    [intermediate_index - 1, intermediate_index], 
                    # , 
                    color='blue', 
                    alpha=alpha, 
                    linewidth=3
                )
            # norm = plt.Normalize(0, intermediate_index)
            # print(f"Intermediate index: {intermediate_index}")
            # prev_intermediates = intermediate_values[sample_index][:intermediate_index]
            # next_intermediates = intermediate_values[sample_index][1: intermediate_index + 1]
            # prev_intermediates = prev_intermediates.reshape(-1, 1, 2)
            # next_intermediates = next_intermediates.reshape(-1, 1, 2)
            # print(f"Prev intermediates shape: {prev_intermediates.shape}")
            # print(f"Next intermediates shape: {next_intermediates.shape}")
            # segments = np.concatenate([prev_intermediates, next_intermediates], axis=1)
            # lc = LineCollection(segments, cmap='Reds', norm=norm, capstyle='round', joinstyle='round')
            # lc.set_array(
            #     np.linspace(0, intermediate_index, num=intermediate_index)
            # )
            # lc.set_linewidth(3)
            # plt.gca().add_collection(lc)
            

        plt.legend(loc='lower center', bbox_to_anchor=(1, 1), ncol=2)

    # Make the animation
    anim = FuncAnimation(plt.gcf(), animate, frames=num_inference_steps // plot_every_n_steps, interval=20)
    # Save the animation
    anim.save('plots/sample_animation.mp4', writer='ffmpeg', fps=30, dpi=500)