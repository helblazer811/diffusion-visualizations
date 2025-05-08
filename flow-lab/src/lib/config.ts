import { FlowModel } from "$lib/diffusion/flow_matching";

export const hyperparameterMenuConfig = {
    "Training Objective": {
        name: "Training Objective",
        options: [
            "Flow Matching",
            "Diffusion"
        ],
        default: "Flow Matching",
    },
    "Number of Steps": {
        name: "Number of Steps",
        options: [
            50,
            100
        ],
        default: 50,
    },
    "Sampler": {
        name: "Sampler",
        options: [
            "Euler",
        ],
        default: "Euler",
    }
};

export const pretrainedModelPaths = {
    "Flow Matching": "/models/flow_matching_model.json",
    "Diffusion": "/models/diffusion_model.json",
}

export const modelTypeToModelClass = {
    "Flow Matching": FlowModel
};

export const modelConfig = {
    "Flow Matching": {
        dim: 2,
        hidden: 64,
    },
    "Diffusion": {
        dim: 2,
        hidden: 64,
    }
};

export const trainingConfig = {
    iterations: 1000,
    batchSize: 256,
}

export const datasetNameToPath = {
    "Three Modes": "/datasets/three_modes.json",
};

export const userInterfaceConfig = {};