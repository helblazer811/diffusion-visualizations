<script lang="ts">
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    import * as tf from '@tensorflow/tfjs';
    
    export let currentTime: number = 0.0; // Default value for the time
    export let isPlaying: boolean = false; // Flag to indicate if the animation is playing
    export let targetDistributionSamples = tf.tensor([]); // Number of samples to generate
    export let sourceDistributionSamples = tf.tensor([]); // Number of samples to generate
    export let currentDistributionSamples = tf.tensor([]); // Number of samples to generate
    export let canvasWidth: number = 1400; // Width of the canvas
    export let canvasHeight: number = 600; // Height of the canvas
    const singleTimeCanvasWidth = canvasHeight;

    // let canvas: HTMLCanvasElement;
    // let ctx;
    let svgElement: SVGSVGElement;

    function plotContour(
        data: tf.Tensor,
        opacity: number = 0.5,
        xLocation: number = 0,
        nx: number = 50,
        ny: number = 50,
    ) {
        // Convert data to plain 2d array
        let values = data.arraySync() as number[][];

        // 2. Build histogram
        const points = values;
        let xMin = d3.min(points, d => d[0]);
        let xMax = d3.max(points, d => d[0]);
        let yMin = d3.min(points, d => d[1]);
        let yMax = d3.max(points, d => d[1]);
        const dataWidth = xMax - xMin;
        const dataHeight = yMax - yMin;
        xMin = xMin - 0.1 * dataWidth;
        xMax = xMax + 0.1 * dataWidth;
        yMin = yMin - 0.1 * dataHeight;
        yMax = yMax + 0.1 * dataHeight; 
        const xScale = d3.scaleLinear().domain([xMin, xMax]).range([0, singleTimeCanvasWidth]);
        const yScale = d3.scaleLinear().domain([yMin, yMax]).range([0, singleTimeCanvasWidth]);

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

    onMount(() => {
        // Set up canvas
        // ctx = canvas.getContext("2d");
        // Plot contours 
        // plotContour(targetDistributionSamples)
        // svgElement = d3.select
    });

    // Run the plot contour if targetDistributionSamples changes
    $: if (targetDistributionSamples && svgElement || currentDistributionSamples && svgElement) {
        // Clear existing contours
        const svg = d3.select(svgElement);
        svg.selectAll("*").remove(); // Clear previous contours
        // Plot the source distribution
        plotContour(sourceDistributionSamples, 0.15, 0);
        // Plot the target distribution
        plotContour(targetDistributionSamples, 0.15, 800);
        // Plot the current distribution
        // First compute the x location based on the current time
        const xLocation = currentTime * (canvasWidth - singleTimeCanvasWidth);
        plotContour(currentDistributionSamples, 1.0, xLocation);
    }

</script>

<div class="marginal-flow-canvas">
    <!-- <canvas id="densityCanvas" bind:this={canvas} width="0" height="0"></canvas> -->
    <svg bind:this={svgElement} width={canvasWidth} height={canvasHeight}></svg>   
</div>