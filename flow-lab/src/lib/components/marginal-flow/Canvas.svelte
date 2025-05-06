<script lang="ts">
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    import * as tf from '@tensorflow/tfjs';
    
    export let currentTime: number = 0.0; // Default value for the time
    export let isPlaying: boolean = false; // Flag to indicate if the animation is playing
    export let targetDistributionSamples = tf.tensor([]); // Number of samples to generate

    let canvas: HTMLCanvasElement;
    let ctx;

    function plotContour(
        data: tf.Tensor,
        width: number = 800,
        height: number = 800,
        nx: number = 50,
        ny: number = 50
    ) {
        console.log('Plotting contour');
        // Convert data to plain 2d array
        let values = data.arraySync() as number[][];

        // 2. Build histogram
        const xBins = nx;
        const yBins = ny;
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
        const xScale = d3.scaleLinear().domain([xMin, xMax]).range([0, width]);
        const yScale = d3.scaleLinear().domain([yMin, yMax]).range([0, height]);

        const contours = d3.contourDensity()
            .x(d => xScale(d[0]))
            .y(d => yScale(d[1]))
            .size([width, height])
            .bandwidth(30)
            .thresholds(4)
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
            .attr("stroke-opacity", 0.5)
    }

    onMount(() => {
        // Set up canvas
        ctx = canvas.getContext("2d");
        // Plot contours 
        // plotContour(targetDistributionSamples)
    });

    // Run the plot contour if targetDistributionSamples changes
    $: if (targetDistributionSamples) {
        if (ctx) {
            ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
            plotContour(targetDistributionSamples);
            // let data = targetDistributionSamples.arraySync() as number[][];
            // // P
            // const ctx = canvas.getContext("2d");

            // const width = canvas.width;
            // const height = canvas.height;
            // const margin = { top: 20, right: 30, bottom: 30, left: 40 };

            // const xScale = d3.scaleLinear()
            //     .domain([d3.min(data, d => d[0]), d3.max(data, d => d[0])])
            //     .range([margin.left, width - margin.right]);

            // const yScale = d3.scaleLinear()
            //     .domain([d3.min(data, d => d[1]), d3.max(data, d => d[1])])
            //     .range([height - margin.bottom, margin.top]); // y-axis flipped

            // // Draw points
            // ctx.fillStyle = "steelblue";
            // data.forEach(([x, y]) => {
            //     ctx.beginPath();
            //     ctx.arc(xScale(x), yScale(y), 5, 0, 2 * Math.PI);
            //     ctx.fill();
            // });
        }
    }

</script>

<div class="marginal-flow-canvas">
    <canvas id="densityCanvas" bind:this={canvas} width="0" height="0"></canvas>
    <svg width="800" height="800"></svg>   
</div>