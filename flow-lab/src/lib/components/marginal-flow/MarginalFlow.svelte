<script lang="ts">
    import Slider from '$lib/components/marginal-flow/Slider.svelte';
    import Canvas from '$lib/components/marginal-flow/Canvas.svelte';
    import * as flow from '$lib/flow-model/model.ts'; // Import the flow model
    import { sampleGaussianMixture, sampleMultivariateNormal } from '$lib/flow-model/helpers.ts'; // Import the utility function
    import { onMount } from 'svelte';
    import * as tf from '@tensorflow/tfjs';

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
    let targetDistributionSamples;
    let sourceDistributionSamples;
    let currentDistributionSamples;
    let allTimeSamples;

    // Load up the cached flow model 
    onMount(async () => {
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
        allTimeSamples = flowModel.sample(numSamples, numTimeSteps);
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
    <Canvas {currentTime} {isPlaying} {targetDistributionSamples} {sourceDistributionSamples} {currentDistributionSamples} {canvasWidth} {canvasHeight}/>
    <Slider bind:value={currentTime} />
</div>