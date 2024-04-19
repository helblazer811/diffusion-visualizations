# Diffusion Visualizations
![Alt Text](media/logo.gif)

For now this repository is a collection of visualizations that I have been putting together of diffusion models. Feel free to extend them or use them. 

# Visualizations 

### Langevin Monte Carlo

Langevin Monte Carlo allows you to sample from a probability distribution using its log gradient ∇ log p(x). This is very useful when a distribution is difficult to sample from directly, but you have information about it's gradient (as is true in many deep learning based techniques). 

By performing a sort of gradient ascent with noise you can navigate around the distribution. Adding noise intuitively prevents the gradient ascent process from converging to one of the modes of the distribution.

Langevin MC draws on methods from statistical physics and is heavily related to modern diffusion models. Diffusion models approximate this log gradient (also called the score) using a neural network.

Abdul Fatir has a great blog post that goes much more in depth on this topic [here](https://abdulfatir.com/blog/2020/Langevin-Monte-Carlo/). 

https://github.com/helblazer811/diffusion-visualizations/assets/14181830/df5409fd-19fa-4184-a65c-70355882d078

Some of the code to construct this is in ```visualizations```. 

### Denoising Diffusion Probabilistic Models

Diffusion models allow a user to sample from a distribution. Unlike Langevin Dynamics, we don't need to actually know the true log gradient of a distribution, but can instead approximate it with a neural network. 

https://github.com/helblazer811/diffusion-visualizations/assets/14181830/78389b38-a6b4-449a-a11b-3dcd1bdfe7ba


Here is a visualization of points being sampled from a simple 2D distribution using a diffusion model. 

Can you guess what the shape of the distribution is haha?

https://github.com/helblazer811/diffusion-visualizations/assets/14181830/47ec6d38-35e2-4a6e-b84f-aa3650f82458

