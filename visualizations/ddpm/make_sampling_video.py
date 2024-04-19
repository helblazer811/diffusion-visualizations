from train import make_spiral_data, DiffusionModel
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import torch
import seaborn as sns
import pandas as pd

if __name__ == "__main__":
    # Load the diffusion model
    diffusion_model = DiffusionModel()
    diffusion_model.load_state_dict(torch.load('models/model.pth'))
    # Load the data
    spiral_data = make_spiral_data(num_examples=500, noise=0.5)
    # Show generation of samples from it using the trained diffusion model
    # Black background figure
    plt.figure(figsize=(5, 5))
    plt.ylim(-4, 4)
    plt.xlim(-4, 4.5)
    # Plot the spiral data
    # plt.scatter(spiral_data[:, 0], spiral_data[:, 1], alpha=0.3, label="Ground Truth Data")
    spiral_data = spiral_data.detach().numpy()
    # plt.hist2d(spiral_data[:, 0], spiral_data[:, 1], bins=1000, cmap='viridis', density=True, range=[[-4, 4], [-4, 4]])
    # Show the plot
    plt.legend()
    # Show the path of each of the samples moving over time
    # Generate N samples from the model, and save the intermediate paths
    num_samples = 100
    num_inference_steps = 1000
    plot_every_n_steps = 20
    samples, intermediate_values = diffusion_model.sample(num_samples=num_samples, num_timesteps=num_inference_steps)
    # Intermediate values has shape (num_samples, num_inference_steps, 2)
    # Pull out only every 50 samples
    intermediate_values = intermediate_values[:, ::plot_every_n_steps, :]
    # data = pd.DataFrame(spiral_data, columns=['x', 'y'])
    # sns.displot(data=data, x="x", y="y")
    # Now plot the intermediate values
    def animate(i):
        sample_index = i // (num_inference_steps // plot_every_n_steps)
        print(sample_index)
        intermediate_index = i % (num_inference_steps // plot_every_n_steps)
        # Plot a line graph of the samples from sample_start_index to interemdiate_index
        plt.clf()
        plt.ylim(-4, 4)
        plt.xlim(-4, 4.5)
        plt.axis('off')
        plt.scatter(spiral_data[:, 0], spiral_data[:, 1], alpha=0.4, color="#67a9cf", label="Ground Truth Data")
        # plt.hist2d(spiral_data[:, 0], spiral_data[:, 1], bins=100, cmap='viridis', density=True, range=[[-4, 4], [-4, 4]])
        plt.plot(
            intermediate_values[sample_index][:intermediate_index, 0], 
            intermediate_values[sample_index][:intermediate_index, 1], 
            color='#ef8a62', 
            linewidth=2
        )
        # Do a scatter plot of the emperical samples up until the current sample index
        plt.scatter(
            samples[:sample_index, 0],
            samples[:sample_index, 1],
            color='#ef8a62', 
            label="Generated Samples",
            alpha=0.9
        )
        # Plot a quiver for the last sample
        if intermediate_index > 0:
            plt.quiver(
                intermediate_values[sample_index][intermediate_index - 1, 0],
                intermediate_values[sample_index][intermediate_index - 1, 1],
                intermediate_values[sample_index][intermediate_index, 0] - intermediate_values[sample_index][intermediate_index - 1, 0],
                intermediate_values[sample_index][intermediate_index, 1] - intermediate_values[sample_index][intermediate_index - 1, 1],
                color='#ef8a62',
                linewidth=2
            )
        plt.legend(loc='bottom', bbox_to_anchor=(1, 1), ncol=2)

    # Make the animation
    anim = FuncAnimation(plt.gcf(), animate, frames=num_samples * num_inference_steps // plot_every_n_steps, interval=20)
    # Save the animation
    anim.save('plots/sample_animation.mp4', writer='ffmpeg', fps=30, dpi=500)
