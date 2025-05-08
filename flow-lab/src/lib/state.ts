import { writable } from 'svelte/store';
import { hyperparameterMenuConfig } from './config';

export const UIState = writable({
    modelType: hyperparameterMenuConfig["Training Objective"].default,
    datasetName: "Three Modes", // Default dataset name
    currentTime: 0,
});

export const model = writable(null);