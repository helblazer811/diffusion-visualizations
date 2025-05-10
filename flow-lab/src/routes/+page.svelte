<script lang="ts">
    import * as tf from '@tensorflow/tfjs';
    import { setWasmPaths } from '@tensorflow/tfjs-backend-wasm';
    setWasmPaths('/tfjs-backend-wasm/');
    import '@tensorflow/tfjs-backend-wasm'; // Import the WebGL backend for TensorFlow.js

    import * as d3 from 'd3';

    import { onMount } from 'svelte';
    import { get } from 'svelte/store';
    // Load up the application config
    import { 
        pretrainedModelPaths, 
        modelTypeToModelClass, 
        modelConfig, 
        datasetNameToPath, 
        trainingConfig, 
        sourceDistributionSamples,
        targetDistributionSamples,
        currentDistributionSamples,
        allTimeSamples
    } from '$lib/state';
    // Load up the application state
    import { UIState, model } from '$lib/state';
    // Load up the components
    import TimeSlider from '$lib/components/time_slider/TimeSlider.svelte';
    import TrainingBar from '$lib/components/TrainingBar.svelte';
    import DisplayArea from '$lib/components/display_area/DisplayArea.svelte';
    // Import helper tf functions
    import { sampleMultivariateNormal } from '$lib/diffusion/utils';
    import MiniDistribution from '$lib/components/dataset_menu/MiniDistribution.svelte';
    import { FlowModel } from '$lib/diffusion/flow_matching';

    let datasetDict = {};

    function loadDataset(path: string) {
        return fetch(path)
            .then(response => response.json())
            .then(data => {
                // Convert the data to a tensor
                const pointsTensor = tf.tensor(data.points);
                return pointsTensor;
            });
    }

    async function loadModel(modelJSONPath: string) {
        const model = await tf.loadLayersModel(modelJSONPath);
        return model;
    }

    /**
     * Draw samples from the model and update the UI state with the samples
     * @param model The model to sample from
     */
    async function drawSamples(
        model,
        numSamples: number,
        numberOfSteps: number = 1000,
    ) {
        // Sample from the model
        const allSamples = model.sample(
            numSamples,
            numberOfSteps,
        ); // shape [num_time_steps, num_samples, dim]
        // Update the UI state with the all time samples
        allTimeSamples.set(allSamples);
        // Compute the range of the points to use for the domain of each contour map
        let flatAllTimeSamples = tf.reshape(allSamples, [numSamples * UIState.numberOfSteps, 2]); // shape [num_time_steps * num_samples, dim]
        flatAllTimeSamples = flatAllTimeSamples.arraySync();
        const xMin = d3.min(flatAllTimeSamples, d => d[0]);
        const xMax = d3.max(flatAllTimeSamples, d => d[0]);
        const yMin = d3.min(flatAllTimeSamples, d => d[1]);
        const yMax = d3.max(flatAllTimeSamples, d => d[1]);
        const domainRange = {
            xMin: xMin - 0.01 * (xMax - xMin),
            xMax: xMax + 0.01 * (xMax - xMin),
            yMin: yMin - 0.01 * (yMax - yMin),
            yMax: yMax + 0.01 * (yMax - yMin),
        };
        UIState.update(state => ({
            ...state,
            domainRange: domainRange,
        }));
    }

    onMount(async () => {
        const readonlyUIState = get(UIState);
        // Load up each of the datasets
        for (const [name, path] of Object.entries(datasetNameToPath)) {
            const pointsTensor = await loadDataset(path);
            datasetDict = { ...datasetDict, [name]: pointsTensor }; // triggers Svelte reactivity
            // console.log(`Loaded dataset ${name} from ${path}`);
            // console.log(`Dataset ${name} shape: `, pointsTensor.shape);
        }
        // Load up the default cached model
        const defaultModelType = readonlyUIState.modelType;
        const defaultDataset: string = readonlyUIState.datasetName;
        const defaultModelPath: string = pretrainedModelPaths[defaultModelType][defaultDataset];
        console.log("Loading model from: ", defaultModelPath);
        const tfModel = await loadModel(defaultModelPath); 
        // Get the model class from the model type
        const modelClass = modelTypeToModelClass[defaultModelType];
        // Initialize the model
        const ourModel = new modelClass(
            modelConfig[defaultModelType]["dim"],
            modelConfig[defaultModelType]["hidden"],
        );
        // Insert the tf model into the model
        ourModel.setModel(tfModel);
        console.log("Model loaded: ", ourModel);
        // Call the dummy worker thread 
        const worker = new Worker(
            new URL('$lib/diffusion/workers/sampling_worker.ts', import.meta.url),
            { type: 'module' }
        );
        worker.postMessage({
            type: 'sample',
            // model: ourModel,
            // numSamples: readonlyUIState.numSamples,
            // numberOfSteps: readonlyUIState.numberOfSteps,
        });
        // Draw samples with the model
        drawSamples(ourModel, readonlyUIState.numSamples, readonlyUIState.numberOfSteps);
        // // Train default model type
        // const defaultModelType = readonlyUIState.modelType;
        // Load up the chosen training dataset points as tf tensor
        const pointsTensor = datasetDict[readonlyUIState.datasetName];
        // Update the UI state with the training dataset
        targetDistributionSamples.set(pointsTensor);
        // // Draw some gaussian samples to put into the UI state as well
        const multivariateNormalSamples = sampleMultivariateNormal(
            [0, 0],
            [[1, 0], [0, 1]],
            readonlyUIState.numSamples
        );
        // Update the UI state with the source distribution samples
        sourceDistributionSamples.set(multivariateNormalSamples);
        // // Load up a model from a file
        // // Train the model
        // console.log('Training model...');
        // ourModel.train(
        //     pointsTensor,
        //     trainingConfig["iterations"],
        //     trainingConfig["batchSize"],
        // ).then(async () => {
        //     // Set up tfjs to use the WebGL backend
        //     await tf.setBackend('wasm');
        //     await tf.ready();
        //     console.log('Model trained successfully');
        //     // Save the model into the model store
        //     model.set(ourModel);
        //     // Save the model to the specified path
        //     // model.save(defaultModelPath);
        //     // Now draw all time samples from the model and put them into the UI state
        //     console.log('Sampling from the model...');
        //     const allSamples = ourModel.sample(
        //         readonlyUIState.numSamples,
        //         readonlyUIState.numberOfSteps,
        //     ); // shape [num_time_steps, num_samples, dim]
        //     // Update the UI state with the all time samples
        //     allTimeSamples.set(allSamples);
        //     // Compute the range of the points to use for the domain of each contour map
        //     let flatAllTimeSamples = tf.reshape(allSamples, [readonlyUIState.numSamples * readonlyUIState.numberOfSteps, 2]); // shape [num_time_steps * num_samples, dim]
        //     flatAllTimeSamples = flatAllTimeSamples.arraySync();
        //     const xMin = d3.min(flatAllTimeSamples, d => d[0]);
        //     const xMax = d3.max(flatAllTimeSamples, d => d[0]);
        //     const yMin = d3.min(flatAllTimeSamples, d => d[1]);
        //     const yMax = d3.max(flatAllTimeSamples, d => d[1]);
        //     const domainRange = {
        //         xMin: xMin - 0.01 * (xMax - xMin),
        //         xMax: xMax + 0.01 * (xMax - xMin),
        //         yMin: yMin - 0.01 * (yMax - yMin),
        //         yMax: yMax + 0.01 * (yMax - yMin),
        //     };
        //     UIState.update(state => ({
        //         ...state,
        //         domainRange: domainRange,
        //     }));
        //     // Download the flow model
        //     // ourModel.download()
        // }).catch((error) => {
        //     console.error('Error training the model:', error);
        // });
    });

</script>

<style>
    .title {
        margin: 0;
        margin-left: 30px;
        font-size: 3.0em;
        color: white;
        font-family: var(--font-family);
    }

    .title-container {
        height: 70px;
        width: 100%;
        background-color: var(--dark-blue);
        display: flex;
        justify-content: center;
        align-items: center;
        /* max-width: var(--inner-component-width); */
        /* margin: 0 auto; */
    }

    .title-left {
        flex: 1;
        height: 100%;
    }

    .title-right {
        flex: 1;
    }

    .title-center {
        height: 100%;
        width: 1400px;
        display: flex;
        flex-direction: row;
        /* justify-content: center; */
        align-items: center;
    }

    /* .sub-title-inner-container {
        display: flex;
        align-items: center;
        height: 100%;
        width: var(--inner-component-width);
    } */

    .sub-title {
        margin: 0 auto;
        font-size: 1.9em;
        color: white;
        font-family: var(--font-family);
        font-weight: 200; /* Thin font */
        /* text-align: right; */
        vertical-align: middle;
    }

    .main-area {
        background-color: var(--light-gray);
        height: 680px;
        display: flex;
    }

    .main-area-left {
        /* width: 20%; */
        flex: 1;
        background-color: var(--light-gray);
    }

    .main-area-center {
        width: 1400px;
    }

    .main-area-right {
        flex: 1;
        background-color: var(--light-gray);
        display: flex;
        flex-direction: column;
        align-items: left;      /* Center items vertically */
        justify-content: center;
        gap: 20px;                /* Add space between items */
        padding-bottom: 100px;
    }


</style>

<div class="container">
    <div class="title-container">
        <div class="title-left"></div>
        <div class="title-center">
            <p class="title"><b>Diffusion</b>Lab</p>
            <h1 class="sub-title">Learn about diffusion and flow  models with interactive visualization. </h1>
        </div>
        <div class="title-right"></div>
    </div>
    <TrainingBar />
    <div class="main-area">
        <!-- <DisplayOptionsMenu />  Menu of items to choose to collect from -->
        <div class="main-area-left"></div>
        <div class="main-area-center">
            <DisplayArea />  
            <TimeSlider /> 
        </div>
        <div class="main-area-right">
            {#each Object.entries(datasetDict) as [name, data]}
                <MiniDistribution data={data} distributionId={name}/>
            {/each}
        </div>
        <!-- <DatasetMenu />  Dataset selector menu to choose the dataset to train on -->
    </div>
</div>