<script lang="ts">
    import * as d3 from 'd3';
    import * as tf from '@tensorflow/tfjs';
    import katex from 'katex';
    import 'katex/dist/katex.min.css';

    import Heatmap from '$lib/components/display_area/Heatmap.svelte';
    import ContourPlot from '$lib/components/display_area/ContourPlot.svelte';

    
    // export let currentTime: number = 0.0; // Default value for the time
    // export let isPlaying: boolean = false; // Flag to indicate if the animation is playing
    // export let targetDistributionSamples = tf.tensor([]); // Number of samples to generate
    // export let sourceDistributionSamples = tf.tensor([]); // Number of samples to generate
    // export let currentDistributionSamples = tf.tensor([]); // Number of samples to generate
    export let data: number[][]; // Data to plot
    export let xLocation: number = 0; // X location of the contour
    export let opacity: number = 0.5; // Opacity of the contour
    export let labelIsLatex: boolean = false; // Flag to indicate if the label is in LaTeX format
    export let label: string; // Label for the distribution
    export let distributionId: string; // ID for the distribution canvas
    export let colorMap: string = "Blues"; // Color map for the heatmap
    export let displayMode: string = "contour"; // Display mode for the distribution

    function displayLatex(
        formula: string,
        xLocation: number,
        yLocation: number,
        distributionId: string = "target",
    ) {
        const svg = d3.select("svg");

        let group = svg.select(`#${distributionId}_latex`);
        if (group.empty()) {
            group = svg.append("foreignObject")
                .attr("id", distributionId + "_latex");
        } else {
            group.selectAll("*").remove();
        }

        group.attr("x", xLocation)
            .attr("y", yLocation)
            .attr("width", 300)
            .attr("height", 100);

        const div = group.append("xhtml:div")
            .style("width", "100%")
            .style("height", "100%")
            .style("display", "flex")
            .style("align-items", "center")
            .style("justify-content", "center")
            .style("font", "34px 'KaTeX_Main', serif")
            .style("color", "#7b7b7b");

        katex.render(formula, div.node(), {
            throwOnError: false
        });
    }

    function displayText(
        text: string,
        xLocation: number,
        yLocation: number,
        distributionId: string = "target",
    ) {
        // Select the group by ID, or create if not exists
        const svg = d3.select("svg");
        // NOTE: This prevents unwanted recreation of the group
        let group = svg.select(`#${distributionId}_text`);
        if (group.empty()) {
            group = svg.append("g").attr("id", distributionId+"_text");
        } else {
            group.selectAll("*").remove(); // Clear previous contents of this group
        }
        // Plot title above the contour 
        group.append("text")
            .attr("x", xLocation)
            .attr("y", yLocation)
            .attr("text-anchor", "middle")
            .style("font-size", "24px")
            .style("font-family", "Helvetica, sans-serif")
            .style("fill", "#7b7b7b")
            .text(text);
    }

</script>

<style>
</style>

{#if displayMode === "heatmap"}
    <Heatmap
        data={data}
        distributionId={distributionId}
        xLocation={xLocation}
        opacity={opacity}
        colorMap={colorMap}
    />
{:else if displayMode === "contour"}
    <ContourPlot
        data={data}
        distributionId={distributionId}
        xLocation={xLocation}
        opacity={opacity}
        colorMap={colorMap}
    />
{/if}

