<script lang="ts">
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    import * as tf from '@tensorflow/tfjs';
    import katex from 'katex';
    import 'katex/dist/katex.min.css';
    
    export let currentTime: number = 0.0; // Default value for the time
    export let isPlaying: boolean = false; // Flag to indicate if the animation is playing
    export let targetDistributionSamples = tf.tensor([]); // Number of samples to generate
    export let sourceDistributionSamples = tf.tensor([]); // Number of samples to generate
    export let currentDistributionSamples = tf.tensor([]); // Number of samples to generate
    export let canvasWidth: number = 1400; // Width of the canvas
    export let canvasHeight: number = 600; // Height of the canvas
    export let domainRange: object = { xMin: -3, xMax: 3, yMin: -3, yMax: 3 }; // Domain range for the plot
    const singleTimeCanvasWidth = canvasHeight;

    let svgElement: SVGSVGElement;

    function plotContour(
        data: tf.Tensor,
        opacity: number = 0.5,
        xLocation: number = 0,
    ) {
        // Convert data to plain 2d array
        let values = data.arraySync() as number[][];

        // 2. Build histogram
        const points = values;
        const xScale = d3.scaleLinear().domain([domainRange.xMin, domainRange.xMax]).range([0, singleTimeCanvasWidth]);
        const yScale = d3.scaleLinear().domain([domainRange.yMin, domainRange.yMax]).range([0, singleTimeCanvasWidth]);

        const contours = d3.contourDensity()
            .x(d => xScale(d[0]))
            .y(d => yScale(d[1]))
            .size([singleTimeCanvasWidth, singleTimeCanvasWidth])
            .bandwidth(30)
            .thresholds(5)
            (values)

        // 4. Scales for drawing
        const svg = d3.select("svg"); 
        // Prepare a color palette
        const color = d3.scaleSequential(d3.interpolateBlues)
            .domain([0, d3.max(contours, d => d.value) * 1.4]);
        // 5. Draw contours
        svg.insert("g", "g")
            .selectAll("path")
            .data(contours)
            .enter().append("path")
            .attr("d", d3.geoPath())
            .attr("fill", function(d) { return color(d.value); })
            .attr("stroke", "#000")
            .attr("stroke-width", 2)
            .attr("stroke-opacity", opacity)
            .attr("fill-opacity", opacity)
            .attr("transform", `translate(${xLocation}, 0)`) // Apply translation
    }

    // Run the plot contour if targetDistributionSamples changes
    $: if (targetDistributionSamples && svgElement || currentDistributionSamples && svgElement) {
        // Clear existing contours
        const svg = d3.select(svgElement);
        svg.selectAll("*").remove(); // Clear previous contours
        // Plot the source distribution
        plotContour(sourceDistributionSamples, 0.15, 0);
        // Plot title above the contour 
        svg.append("text")
            .attr("x", singleTimeCanvasWidth / 2)
            .attr("y", 50)
            .attr("text-anchor", "middle")
            .style("font-size", "34px")
            .style("font-family", "Helvetica, sans-serif")
            .style("fill", "#7b7b7b")
            .text("Source Distribution");
        // Plot the target distribution
        plotContour(targetDistributionSamples, 0.15, 800);
        // Plot title above the contour
        svg.append("text")
            .attr("x", 800 + singleTimeCanvasWidth / 2)
            .attr("y", 50)
            .attr("text-anchor", "middle")
            .style("font-size", "34px")
            .style("font-family", "Helvetica, sans-serif")
            .style("fill", "#7b7b7b")
            .text("Target Distribution");
        // Plot the current distribution
        // First compute the x location based on the current time
        const xLocation = currentTime * (canvasWidth - singleTimeCanvasWidth);
        plotContour(currentDistributionSamples, 1.0, xLocation);
        // Draw latex over current distribution
        // Only show if the x location is not overlapping with source or target
        if (xLocation > 150 && xLocation < canvasWidth - singleTimeCanvasWidth - 150) {
            // Create a foreignObject to hold HTML
            const fo = svg.append("foreignObject")
                .attr("x", xLocation + singleTimeCanvasWidth / 2 - 150)
                .attr("y", 50 - 52)
                .attr("text-anchor", "middle")
                .attr("width", 300)
                .attr("height", 100)
                .style("margin", "0");

            const div = fo.append("xhtml:div")
                .style("font", "34px 'KaTeX_Main', serif")
                .style("text-align", "center")
                .style("line-height", "100px")
                .style("color", "#7b7b7b")
                .style("border-radius", "5px")
                .style("margin", "0")

            // Render LaTeX inside the div using KaTeX
            const formula = "p_t(x)";
            katex.render(formula, div.node(), {
                throwOnError: false
            });
        }

    }

</script>

<style>
    .katex {
        /* background-color: white; */
    }

    .marginal-flow-canvas {
        width: 100%;
        height: 100%;
        background-color: var(--light-gray);
    }
</style>

<div class="marginal-flow-canvas">
    <!-- <canvas id="densityCanvas" bind:this={canvas} width="0" height="0"></canvas> -->
    <svg bind:this={svgElement} width={canvasWidth} height={canvasHeight}></svg>   
</div>