import { writable } from 'svelte/store';
import { hyperparameterMenuConfig } from './config';

export const UIState = writable({
    modelType: hyperparameterMenuConfig["Training Objective"].default,
    datasetName: "Three Modes",
});

export const model = writable(null);