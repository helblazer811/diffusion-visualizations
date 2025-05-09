<script>
    import * as tf from '@tensorflow/tfjs';

    import { UIState, currentTime } from '$lib/state';
    import { interfaceSettings } from '$lib/state';

    import Distribution from '$lib/components/distribution_canvas/Distribution.svelte';
    let svgElement;
    // const singleTimeCanvasWidth = canvasHeight;
    // // If currentTime changes in the UI state then update the current distribution samples in the UI state
    // $ : {
    //     if (model) { // If the model is loaded, then we can sample from it
    //         // Set up web assembly backend for tensorflow.js
    //         await tf.setBackend('wasm');
    //         await tf.ready();
    //         // Draw some samples from the model
    //         allTimeSamples = flowModel.sample(numSamples, numTimeSteps); // shape [num_time_steps, num_samples, dim]
    //     }
    // }
    // If the currentTime changes then update the current distribution samples in the UI state
    $: if ($currentTime) {
        // Convert current time to index
        let currentTimeIndex = Math.floor($currentTime * $UIState.numberOfSteps);
        console.log("Current time index: ", currentTimeIndex);
        // Avoid going out of bounds
        if (currentTimeIndex >= $UIState.numberOfSteps) {
            currentTimeIndex = $UIState.numberOfSteps - 1;
        }
        // Pull out the current time samples from the all time samples
        const currentSamples = tf.tidy(() => $UIState.allTimeSamples.gather(currentTimeIndex));
        console.log("Current samples shape: ", currentSamples.shape);
        // Update the current distribution samples in the UI state
        UIState.update(state => ({
            ...state,
            currentDistributionSamples: currentSamples
        }));
    }

    $: if ($UIState.currentDistributionSamples) {
        console.log("Current distribution samples: ", $UIState.currentDistributionSamples);
    }

</script>

<style>
    .distribution-canvas-container {
        position: relative;
        width: 100%;
        display: flex;
        justify-content: center;
    }

</style>
  
<div class="distribution-canvas-container">
    <svg 
        bind:this={svgElement} 
        width={interfaceSettings.distributionCanvasWidth} 
        height={interfaceSettings.distributionCanvasHeight}
    ></svg>
    {#if svgElement}
        <Distribution
            svgElement={svgElement}
            data={$UIState.sourceDistributionSamples}
            xLocation={0}
            opacity={0.15}
            label="Source Distribution"
            distributionId="source"
        />
    
        <Distribution
            svgElement={svgElement}
            data={$UIState.targetDistributionSamples}
            xLocation={800}
            opacity={0.15}
            label="Target Distribution"
            distributionId="target"
        />
    
        <Distribution
            svgElement={svgElement}
            data={$UIState.currentDistributionSamples}
            xLocation={$currentTime * (interfaceSettings.distributionCanvasWidth - interfaceSettings.distributionWidth)}
            opacity={1.0}
            label="p_t(x)"
            labelIsLatex={true}
            distributionId="current"
        />
    {/if}
  
</div>