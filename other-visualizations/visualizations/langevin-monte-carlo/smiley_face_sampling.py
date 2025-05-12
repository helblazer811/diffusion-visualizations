import torch
import math
import numpy as np
import matplotlib.pyplot as plt
from torch.distributions import MultivariateNormal
from tqdm import tqdm
from matplotlib.animation import FuncAnimation

plt.style.use('dark_background')
torch.autograd.set_detect_anomaly(True)

def generate_star_samples(num_samples=5000):
    """
        This is used to generate samples from the star distribution
    """
    # Make the covariances
    cov_1 = torch.Tensor([
        [1.0, 0.0],
        [0.0, 0.1]
    ])
    # Rotate 60 degrees
    angle = torch.pi / 3
    rotation_matrix = torch.Tensor([
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
    ])
    cov_2 = rotation_matrix @ cov_1 @ rotation_matrix.T
    # Rotate 60 degrees
    angle = 2 * torch.pi / 3
    rotation_matrix = torch.Tensor([
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
    ])
    cov_3 = rotation_matrix @ cov_1 @ rotation_matrix.T
    # Sample from the distributions
    samples = []
    for i in range(num_samples):
        # Sample from the first distribution
        samples.append(MultivariateNormal(torch.Tensor([0.0, 0.0]), cov_1).sample())
        # Sample from the second distribution
        samples.append(MultivariateNormal(torch.Tensor([0.0, 0.0]), cov_2).sample())
        # Sample from the third distribution
        samples.append(MultivariateNormal(torch.Tensor([0.0, 0.0]), cov_3).sample())
    return torch.stack(samples)

def star_log_pdf(x):
    """
        This is the log probability density function of the star distribution
        NOTE: This must be differentiable with torch. 
    """
    # Make the covariances
    cov_1 = torch.Tensor([
        [1.0, 0.0],
        [0.0, 0.1]
    ])
    # Rotate 60 degrees
    angle = torch.pi / 3
    rotation_matrix = torch.Tensor([
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
    ])
    cov_2 = rotation_matrix @ cov_1 @ rotation_matrix.T
    # Rotate 60 degrees
    angle = 2 * torch.pi / 3
    rotation_matrix = torch.Tensor([
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
    ])
    cov_3 = rotation_matrix @ cov_1 @ rotation_matrix.T
    # Return the sum of the log probabilities
    sum = 0.0
    for cov in [cov_1, cov_2, cov_3]:
        sum += MultivariateNormal(torch.Tensor([0.0, 0.0]), cov).log_prob(x)

    return sum

def smiley_face_pdf(z):
    # z = np.reshape(z, [z.shape[0], 2])
    # Make the mouth
    norm = torch.sqrt(z[:, 0] ** 2 + z[:, 1] ** 2)
    exp1 = torch.exp(-0.5 * ((z[:, 1] + 2) / 0.6) ** 2)
    # exp2 = np.exp(-0.5 * ((z1 + 2) / 0.6) ** 2)
    u = 0.5 * ((norm - 2) / 0.4) ** 2 - torch.log(exp1)
    sum_pdf = torch.exp(-u)
    # Make the eyes
    # Make gaussian pdfs for the eyes
    eye1 = MultivariateNormal(torch.tensor([1.0, 1.0]), torch.eye(2) * 0.1)
    eye2 = MultivariateNormal(torch.tensor([-1.0, 1.0]), torch.eye(2) * 0.1)
    # Compute the pdfs
    eye1_pdf = eye1.log_prob(z)
    eye2_pdf = eye2.log_prob(z)
    # Add the pdfs
    sum_pdf = sum_pdf + 0.5 * torch.exp(eye1_pdf) + 0.5 * torch.exp(eye2_pdf)
    # Draw the nose
    nose = MultivariateNormal(torch.tensor([0.0, -0.4]), torch.eye(2) * 0.1)
    nose_pdf = nose.log_prob(z)
    sum_pdf = sum_pdf + 0.5 * torch.exp(nose_pdf)

    return sum_pdf

def generate_langevin_samples(step_size=0.1, num_samples=5000, burn_in=2000):
    """
        Runs langevin dynamics using the gradient of the star gaussian mixture distribution
        and renders an animation of it. 

        Returns:
            A list of the points traversed by the langevin dynamics, where the final point is the sample
    """
    # Generate initial point uniformly sampled from -3 to 3
    x_init = torch.rand(2) * 6 - 3
    samples = []
    x_current = x_init
    # Set the step size
    for i in tqdm(range(burn_in + num_samples)):
        x_current.requires_grad = True
        # Compute the gradient of the log pdf
        u = torch.log(smiley_face_pdf(x_current.unsqueeze(0)))
        grad = torch.autograd.grad(u, x_current)[0]
        # Do Langevin Dynamics update
        x_current = x_current + step_size * grad + np.sqrt(2 * step_size) * torch.randn(2)
        x_current = x_current.detach()
        if i >= burn_in:
            samples.append(x_current.numpy())

    samples = np.stack(samples)
    return samples

def make_animation():
    """
        Closure for making the entire animation
    """
    # Make the matplotlib axis with two square subplots side by side
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    # Plot the density of the heart
    r = np.linspace(-5, 5, 200)
    x, y = np.meshgrid(r, r)
    z = np.vstack([x.flatten(), y.flatten()]).T
    z = torch.Tensor(z)
    # q0 = npdensity2(z)
    q0 = smiley_face_pdf(z)
    axs[0].pcolormesh(x, y, q0.reshape(x.shape), cmap='viridis')
    # Generate samples using langevin dynamics and animate the path on the left plot and show the final samples on the right.
    num_samples = 5000
    # Generate the samples using langevin dynamics
    samples = generate_langevin_samples(num_samples=num_samples)
    # axs[1].hist2d(samples[:, 0], samples[:, 1], bins=100, cmap='viridis', density=True)
    
    # Set aspect ratio of each subplot
   
    # Make an animation of the markov chain
    # Show only the 100 most recent samples
    def animate(i):
        print(i)
        # Plot all of the samples up to i on the right plot
        axs[1].clear()
        axs[1].hist2d(samples[:i, 0], samples[:i, 1], bins=100, cmap='viridis', density=True, range=[[-3, 3], [-3.5, 2.5]])
        # axs[1].scatter(samples[:i, 0], samples[:i, 1], color='blue', alpha=0.5)
        # Plot the path of the markov chain on the left plot, but only the last 100 samples
        axs[0].clear()
        # Plot the density
        axs[0].pcolormesh(x, y, q0.reshape(x.shape), cmap='viridis', vmin=0)
        axs[0].plot(samples[max(0, i - 50):i, 0], samples[max(0, i - 50):i, 1], color='white', alpha=0.8, linewidth=2)
        # Show the last one as a quiver
        axs[0].quiver(samples[i - 1, 0], samples[i - 1, 1], samples[i, 0] - samples[i - 1, 0], samples[i, 1] - samples[i - 1, 1], color='white', linewidth=2)

        axs[0].set_xlim([-3, 3])
        axs[0].set_ylim([-3.5, 2.5])
        axs[1].set_xlim([-3, 3])
        axs[1].set_ylim([-3.5, 2.5])
        axs[0].set_aspect('equal', adjustable='box')
        axs[1].set_aspect('equal', adjustable='box')
        axs[1].set_xticks([])
        axs[1].set_yticks([])
        axs[0].set_xticks([])
        axs[0].set_yticks([])
        axs[0].spines['top'].set_color('none')
        axs[0].spines['bottom'].set_color('none')
        axs[0].spines['left'].set_color('none')
        axs[0].spines['right'].set_color('none')
        axs[1].spines['top'].set_color('none')
        axs[1].spines['bottom'].set_color('none')
        axs[1].spines['left'].set_color('none')
        axs[1].spines['right'].set_color('none')

    # Make the animation
    anim = FuncAnimation(fig, animate, frames=num_samples, interval=60)
    # Save as a video
    anim.save('langevin_dynamics.mp4', writer='ffmpeg', fps=30)

if __name__ == "__main__":
    make_animation()