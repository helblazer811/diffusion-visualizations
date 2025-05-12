from train import DiffusionModel
import torch
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Load the dino model
    diffusion_model = DiffusionModel()
    diffusion_model.load_state_dict(torch.load('models/dino_model.pth'))
    # Draw N samples from it, saving the intermediates
    num_samples = 500
    _, intermediate_samples = diffusion_model.sample(num_samples=num_samples, num_timesteps=1000)
    # Truncate the first 30 percent of the samples
    intermediate_samples = intermediate_samples[:, 900:, :]
    every_n_steps = 1
    # intermediate_samples = intermediate_samples[:, ::every_n_steps, :]
    # Show all samples moving over time in the video 
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(4, 5))
    plt.subplots_adjust(bottom=0.25)
    # Create a slider 
    ax_slider = plt.axes([0.25, 0.25, 0.55, 0.03])
    slider = Slider(ax_slider, '', 0, 1, valinit=0)
    ax_slider_label = plt.axes([0.5, 0.2, 0.1, 0.03], facecolor='lightgoldenrodyellow')
    ax_slider_label.axis('off')
    ax_slider_label.text(0.5, 0.5, 'Time', verticalalignment='center', horizontalalignment='center', transform=ax_slider_label.transAxes)

    # Initialize empty line
    line, = ax.plot([], [], lw=2)
    # Initialize scatter plot
    scatter = ax.scatter(intermediate_samples[:, 0, 0], intermediate_samples[:, 0, 1], color='#67a9cf', alpha=0.5)
    ax.axis('off')
    # Initialize function to update plot
    def update(t):
        # t = slider.val
        slider.set_val(1 - t / 100)
        # line.set_data([t, t], [0, 0])
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        scatter.set_offsets(intermediate_samples[:, t * every_n_steps, :])

    # fig, ax = plt.subplots()
    # plt.subplots_adjust(bottom=0.25)

    # # Create a slider
    # ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])
    # slider = Slider(ax_slider, 'Time', 0, 10, valinit=0)
    # # Initialize empty line
    # line, = ax.plot([], [], lw=2)   
    # # Make a scatter plot axis for the samples above the other one
    # ax_scatter = plt.axes([0.25, 0.3, 0.65, 0.65])
    # # plt.axis('off')
    # # plt.scatter(intermediate_samples[:, -1, 0], intermediate_samples[:, -1, 1], color='#67a9cf', alpha=0.5)
    # # plt.show()

    # def animate(t):
    #     plt.clf()
    #     # plt.ylim(-3, 3)
    #     # plt.xlim(-2.5, 2.5)
    #     plt.axis('off')
    #     print(t)
    #     # Plot the samples for time t
    #     ax.scatter(intermediate_samples[:, t * every_n_steps, 0], intermediate_samples[:, t * every_n_steps, 1], color='#67a9cf', alpha=0.5)
    #     # Adjust the slider
    #     slider.set_val(t)
    #     # Show the last 5 intermediate samples before t as a line plot
    #     # for i in range(num_samples):
    #     #     plt.plot(intermediate_samples[i, max(0, t - 5):t, 0], intermediate_samples[i, max(0, t - 5):t, 1], color='#67a9cf', alpha=0.2)
        
    # Create animation
    # fig, ax = plt.subplots(figsize=(5, 5))
    ani = FuncAnimation(fig, update, frames=range(0, 100), interval=50)
    # Save the animation as a video file
    ani.save('plots/dino_samples.mp4', writer='ffmpeg', dpi=500)