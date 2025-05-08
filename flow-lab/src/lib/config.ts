import { writable } from 'svelte/store';

export const config = writable({
    theme: 'light',
    fontSize: 16,
    showGrid: true,
    // Specify the hyperparameter menu
    hyperparameterMenuConfig: [
        {
            name: "Training Objective",
            options: [
                "Flow Matching",
                "Diffusion"
            ],
            default: "Flow Matching",
            current: "Flow Matching"
        },
        {
            name: "Number of Steps",
            options: [
                50,
                100
            ],
            default: 50,
            current: 50
        },
        {
            name: "Sampler",
            options: [
                "Euler",
            ],
            default: "Euler",
            current: "Euler"
        }
    ]
});