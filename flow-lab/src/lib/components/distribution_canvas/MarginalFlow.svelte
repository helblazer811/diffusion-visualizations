<script lang="ts">
    import Slider from '$lib/components/marginal-flow/Slider.svelte';
    import Canvas from '$lib/components/marginal-flow/Canvas.svelte';
    import { sampleGaussianMixture, sampleMultivariateNormal } from '$lib/diffusion/utils.ts';
    import { onMount } from 'svelte';
    import * as d3 from 'd3';

    import * as tf from '@tensorflow/tfjs';
    // import { env } from '@tensorflow/tfjs-core';
    import { setWasmPaths } from '@tensorflow/tfjs-backend-wasm';
    setWasmPaths('/tfjs-backend-wasm/');

    import '@tensorflow/tfjs-backend-wasm'; // Import the WebGL backend for TensorFlow.js


    // Props for the MarginalFlow component
    export let currentTime: number = 0.0; // Default value for the time
    export let isPlaying: boolean = true; // Flag to indicate if the animation is playing

    // Local file variables
    const frameRate: number = 45; // Frame rate for the animation
    const numSamples: number = 10000; // Number of samples to generate
    const hiddenDim: number = 64; // Hidden dimension for the flow model
    const canvasWidth: number = 1400; // Width of the canvas
    const canvasHeight: number = 600; // Height of the canvas
    const numTimeSteps: number = 300; // Number of time steps for the flow model
    let flowModelPath: string = '/models/flow_model.json'; // Path to the flow model
    let flowModel: flow.FlowModel; // Flow model object
    let targetDistributionSamples: tf.Tensor; // Target distribution samples
    let sourceDistributionSamples: tf.Tensor; // Source distribution samples
    let currentDistributionSamples: tf.Tensor; // Current distribution samples
    let allTimeSamples: tf.Tensor[]; // All time samples from the flow model
    let domainRange: object = { xMin: -3, xMax: 3, yMin: -3, yMax: 3 }; // Domain range for the plot

    // Load up the cached flow model 
    onMount(async () => {
        // Set up tfjs to use the WebGL backend
        await tf.setBackend('wasm');
        await tf.ready();
        // Load or train and load the flow model. 
        // flow.loadFlowModel(flowModelPath).then((model) => {
        //     if (model) {
        //         console.log('Flow model loaded successfully.');
        //         flowModel = model;
        //     } else {
        //         // Train the flow model
        //         console.log('Training flow model...');
        //         flowModel = flow.trainFlowModel();
        //         // Cache the flow model to the specified path
        //         flow.downloadFlowModel(flowModel);
        //     } 
        // })
        // Generate dataset (target distribution)
        targetDistributionSamples = sampleGaussianMixture(numSamples);
        // Generate source distributions samples (isotropic Gaussian)
        sourceDistributionSamples = sampleMultivariateNormal(
            [0, 0],
            [[1, 0], [0, 1]],
            numSamples,
        );
        // Initialize the current distribution to the source distribution
        // currentDistributionSamples = sourceDistributionSamples;
        // targetDistributionSamples = sampleMultivariateNormal(numSamples, 2, 0.5);
        // Train the flow model
        console.log("Training the flow model");
        flowModel = flow.trainFlowModel(
            targetDistributionSamples,
            2,
            hiddenDim,
            2000,
            64,
        );
        // Here run simulate the trajectories of the flow model and save all of the timesteps
        console.log("Sampling from the flow model");
        allTimeSamples = flowModel.sample(numSamples, numTimeSteps); // shape [num_time_steps, num_samples, dim]
        // Compute the range of the points to use for the domain of each contour map
        let flatAllTimeSamples = tf.reshape(allTimeSamples, [numSamples * numTimeSteps, 2]); // shape [num_time_steps * num_samples, dim]
        flatAllTimeSamples = flatAllTimeSamples.arraySync();
        const xMin = d3.min(flatAllTimeSamples, d => d[0]);
        const xMax = d3.max(flatAllTimeSamples, d => d[0]);
        const yMin = d3.min(flatAllTimeSamples, d => d[1]);
        const yMax = d3.max(flatAllTimeSamples, d => d[1]);
        domainRange = {
            xMin: xMin - 0.01 * (xMax - xMin),
            xMax: xMax + 0.01 * (xMax - xMin),
            yMin: yMin - 0.01 * (yMax - yMin),
            yMax: yMax + 0.01 * (yMax - yMin),
        }
        console.log("Domain range: ", domainRange);
        // Pull out the first timestep samples
        currentDistributionSamples = tf.gather(allTimeSamples, 0); // shape [num_samples, dim]
        // Set up an interval to increase the timer periodically
        const interval = setInterval(() => {
            if (isPlaying) {
                currentTime += 1.0 / numTimeSteps; // Increment the time in the flow sense. 
                if (currentTime > 1) {
                    currentTime = 0;
                }
                // Update the current distribution samples based on the current time
                currentDistributionSamples = tf.gather(allTimeSamples, Math.floor(currentTime * numTimeSteps));
            }
        }, 1000 / frameRate); // 1000 ms / frameRate = interval in ms
        // Clear the interval when the component is destroyed
        return () => {
            clearInterval(interval);
        };
    });
    
    // Set up something to react when current Time changes to update the current distribution samples
    $: if (currentTime && allTimeSamples) {
        let currentTimeIndex = Math.floor(currentTime * numTimeSteps);
        if (currentTimeIndex >= numTimeSteps) {
            currentTimeIndex = numTimeSteps - 1;
        }
        // Update the current distribution samples based on the current time
        currentDistributionSamples = tf.gather(allTimeSamples, currentTimeIndex); // shape [num_samples, dim]);
    }

</script>

<style>
    /* Center the text in the div */
    .marginal-flow {
        width: 1400px; /* Fixed width */
        height: 600px; /* Fixed height */
        margin: 0 auto; /* Center the div horizontally */
    }
</style>

<div class="marginal-flow">
    <Canvas {currentTime} {isPlaying} {targetDistributionSamples} {sourceDistributionSamples} {currentDistributionSamples} {canvasWidth} {canvasHeight} {domainRange}/>
    <Slider bind:value={currentTime} />
</div>