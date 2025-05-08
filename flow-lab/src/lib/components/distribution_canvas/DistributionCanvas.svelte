<script>
    import Distribution from '$lib/components/Distribution.svelte';
    let svgElement;
    const singleTimeCanvasWidth = canvasHeight;

    // If currentTime changes in the UI state then update the current distribution samples

</script>
  
  <svg bind:this={svgElement} width={canvasWidth} height={canvasHeight}></svg>
  
  {#if svgElement}
    <Distribution
        svgElement={svgElement}
        data={sourceDistributionSamples}
        xLocation={0}
        opacity={0.15}
        label="Source Distribution"
        domainRange={domainRange}
        canvasSize={singleTimeCanvasWidth}
    />
  
    <Distribution
        svgElement={svgElement}
        data={targetDistributionSamples}
        xLocation={800}
        opacity={0.15}
        label="Target Distribution"
        domainRange={domainRange}
        canvasSize={singleTimeCanvasWidth}
    />
  
    {#if currentDistributionSamples}
        {#if currentTime > 150 / canvasWidth && currentTime < 1 - 150 / canvasWidth}
            <Distribution
                svgElement={svgElement}
                data={currentDistributionSamples}
                xLocation={currentTime * (canvasWidth - singleTimeCanvasWidth)}
                opacity={1.0}
                label="p_t(x)"
                domainRange={domainRange}
                canvasSize={singleTimeCanvasWidth}
            />
        {/if}
    {/if}
{/if}
  