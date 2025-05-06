<script lang="ts">
    import Slider from '$lib/components/marginal-flow/Slider.svelte';
    import Canvas from '$lib/components/marginal-flow/Canvas.svelte';
    import * as flow from '$lib/flow-model/model.ts'; // Import the flow model
    import { sampleGaussianMixture, sampleMultivariateNormal } from '$lib/flow-model/helpers.ts'; // Import the utility function
    import { onMount } from 'svelte';

    // Props for the MarginalFlow component
    export let currentTime: number = 0.0; // Default value for the time
    export let isPlaying: boolean = false; // Flag to indicate if the animation is playing

    // Local file variables
    let numSamples: number = 10000; // Number of samples to generate
    let hiddenDim: number = 64; // Hidden dimension for the flow model
    let flowModelPath: string = '/models/flow_model.json'; // Path to the flow model
    let flowModel; // Flow model object
    let targetDistributionSamples;

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
        // Generate dataset
        targetDistributionSamples = sampleGaussianMixture(numSamples);
        console.log(targetDistributionSamples)
        // targetDistributionSamples = sampleMultivariateNormal(numSamples, 2, 0.5);
        // Train the flow model
        // flowModel = flow.trainFlowModel(
        //     dataset,
        //     2,
        //     hiddenDim,
        //     10000,
        //     64,
        // );
    });

</script>

<style>
    /* Center the text in the div */
    .marginal-flow {
        width: 1400px; /* Fixed width */
        height: 800px; /* Fixed height */
        margin: 0 auto; /* Center the div horizontally */
    }
</style>

<div class="marginal-flow">
    <Canvas {currentTime} {isPlaying} {targetDistributionSamples} />
    <Slider bind:value={currentTime} />
</div>