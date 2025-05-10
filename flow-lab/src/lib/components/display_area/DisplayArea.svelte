<script>
    import * as tf from '@tensorflow/tfjs';

    import { UIState, currentTime, sourceDistributionSamples} from '$lib/state';
    import { interfaceSettings } from '$lib/state';

    import Distribution from '$lib/components/display_area/Distribution.svelte';
    
    // If the currentTime changes then update the current distribution samples in the UI state
    $: if ($currentTime) {
        // Convert current time to index
        let currentTimeIndex = Math.floor($currentTime * $UIState.numberOfSteps);
        // Avoid going out of bounds
        if (currentTimeIndex >= $UIState.numberOfSteps) {
            currentTimeIndex = $UIState.numberOfSteps - 1;
        }
        // Pull out the current time samples from the all time samples
        const currentSamples = tf.tidy(() => $UIState.allTimeSamples.gather(currentTimeIndex));
        // Update the current distribution samples in the UI state
        UIState.update(state => ({
            ...state,
            currentDistributionSamples: currentSamples
        }));
    }

</script>

<style>
    .display-area {
        position: relative;
    }
</style>

<div 
    class="display-area" 
    style="width: {interfaceSettings.displayAreaWidth}px; height: {interfaceSettings.displayAreaHeight}px;"
>
    <Distribution
        data={$sourceDistributionSamples}
        xLocation={0}
        opacity={1.0}
        label="Source Distribution"
        distributionId="source"
    />
    <!-- <Distribution
        data={$UIState.targetDistributionSamples}
        xLocation={800}
        opacity={0.15}
        label="Target Distribution"
        distributionId="target"
    />
    <Distribution
        data={$UIState.currentDistributionSamples}
        xLocation={$currentTime * (interfaceSettings.displayAreaWidth - interfaceSettings.distributionWidth)}
        opacity={1.0}
        label=""
        labelIsLatex={true}
        distributionId="current"
    /> -->
</div>