import torch
from train import make_spiral_data, DiffusionModel

import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Import the trained DM
    diffusion_model = DiffusionModel()
    diffusion_model.load_state_dict(torch.load('models/model.pth'))
    # Load the spiral training data
    spiral_data = make_spiral_data(num_examples=1000, noise=0.0)
    # Sample the score in linearly spaced intervals in the range of the trianing data
    x = torch.linspace(spiral_data[:, 0].min(), spiral_data[:, 0].max(), 30)
    y = torch.linspace(spiral_data[:, 1].min(), spiral_data[:, 1].max(), 30)
    xx, yy = torch.meshgrid(x, y)
    xy = torch.stack([xx, yy], dim=-1).reshape(-1, 2)
    # Sample the score
    # Choose a time near 0 in range [0, 1000]
    time = torch.Tensor([50]).long().repeat(xy.shape[0])
    score = diffusion_model.predict_noise(xy, time)
    # Plot the scores as a quiver plot
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    xy = xy.detach().numpy()
    score = score.detach().numpy()
    ax[0].quiver(xy[:, 0], xy[:, 1], score[:, 0], score[:, 1], scale=100, headwidth=2)
    ax[0].set_title('Evaluation of the Score Function\n at Low Time Scale (Approx 0)')
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    # Plot the data points
    ax[1].scatter(spiral_data[:, 0], spiral_data[:, 1])
    ax[1].set_title('Ground Truth Training Data')
    ax[1].set_xticks([])
    ax[1].set_yticks([])

    plt.savefig('plots/score_plot.png', dpi=300)