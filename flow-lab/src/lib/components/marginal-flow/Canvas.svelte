<script lang="ts">
    import * as d3 from 'd3';
    import { onMount } from 'svelte';
    import * as tf from '@tensorflow/tfjs';
    
    export let currentTime: number = 0.0; // Default value for the time
    export let isPlaying: boolean = false; // Flag to indicate if the animation is playing
    export let targetDistributionSamples = tf.tensor([]); // Number of samples to generate

    let canvas: HTMLCanvasElement;
    let ctx;

    function compute2DHistogram(points, xMin, xMax, yMin, yMax, xBins, yBins) {
        const hist = Array.from({ length: xBins }, () => Array(yBins).fill(0));

        const xBinSize = (xMax - xMin) / xBins;
        const yBinSize = (yMax - yMin) / yBins;

        for (const [x, y] of points) {
            const i = Math.floor((x - xMin) / xBinSize);
            const j = Math.floor((y - yMin) / yBinSize);
            if (i >= 0 && i < xBins && j >= 0 && j < yBins) {
                hist[i][j]++;
            }
        }

        return hist;
    }


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
        const hist = Array.from({ length: yBins }, () => Array(xBins).fill(0));
        const xScale = d3.scaleLinear().domain([xMin, xMax]).range([0, width]);
        const yScale = d3.scaleLinear().domain([yMin, yMax]).range([0, height]);

        // for (const [x, y] of points) {
        //     const i = Math.floor(xScale(x));
        //     const j = Math.floor(yScale(y));
        //     if (i >= 0 && i < xBins && j >= 0 && j < yBins) {
        //         hist[j][i]++;
        //     }
        // }

        // Set up 5 thresholds based on the max of the histogram
        // const maxCount = d3.max(hist.flat());
        // const thresholds = d3.range(1, maxCount, 5);

        // 3. Flatten histogram and generate contours
        // values = hist.flat();
        // const contours = d3.contours()
        //     .size([xBins, yBins])
        //     .thresholds(thresholds)
        //     (values);

        const contours = d3.contourDensity()
            .x(d => xScale(d[0]))
            .y(d => yScale(d[1]))
            .size([width, height])
            .bandwidth(20)
            (values)

        // 4. Scales for drawing
        const svg = d3.select("svg");
        // const cellWidth = width / xBins;
        // const cellHeight = height / yBins;
        // const xDraw = d3.scaleLinear().domain([0, xBins]).range([0, width]);
        // const yDraw = d3.scaleLinear().domain([0, yBins]).range([0, height]);
        // Setup color scheme
        // const color = d3.scaleSequential()
        //     .domain([0, d3.max(values)])
        //     .interpolator(d3.interpolateOrRd);
                
        // Prepare a color palette
        var color = d3.scaleLinear()
            .domain([0, 0.1]) // Points per square pixel.
            .range(["white", "#69b3a2"]);
        // 5. Draw contours
        svg.insert("g", "g")
            .selectAll("path")
            .data(contours)
            .enter().append("path")
            .attr("d", d3.geoPath())
            .attr("fill", function(d) { return color(d.value); })
        // svg.selectAll("path")
        //     .data(contours)
        //     .join("path")
        //     .attr("d", d3.geoPath(d3.geoIdentity().scale(cellWidth)))
        //     .attr("fill", d => color(d.value))
        //     .attr("stroke", "steelblue")
        //     .attr("stroke-width", 1.5);
        // Generate contour thresholds (you can customize this)
        // Convert the values to a 2D grid
        // const bins = 40;
        // const xMin: number = d3.min(values, d => d[0]);
        // const xMax: number = d3.max(values, d => d[0]);
        // const yMin: number = d3.min(values, d => d[1]);
        // const yMax: number = d3.max(values, d => d[1]);
        // const hist = compute2DHistogram(values, xMin, xMax, yMin, yMax, bins, bins);
        // // Normalize the histogram by the total number of values
        // console.log(hist)
        // // Make thresholds
        // // const thresholds = d3.range(0, 1, 0.1).map(d => d * d3.max(hist.flat()));
        // const thresholds = d3.range(1, 20, 1);
        // // Generate contours from data
        // const contours = d3.contours()
        //     // .bandwidth(10)
        //     .size([bins, bins])
        //     .thresholds(thresholds)(hist);

        // // Define scaling from grid to canvas coordinates
        // // const xScale = d3.scaleLinear().domain([-nx, nx]).range([0, width]);
        // // const yScale = d3.scaleLinear().domain([-ny, ny]).range([0, height]);

        // const margin = { top: 20, right: 30, bottom: 30, left: 40 };
        // const xScale = d3.scaleLinear()
        //     .domain([0, bins])
        //     .range([0, width]); // x-axis flipped

        // const yScale = d3.scaleLinear()
        //     .domain([0, bins])
        //     .range([0, height]); // y-axis flipped

        // // Draw contours
        // contours.forEach(contour => {
        //     ctx.beginPath();
        //     contour.coordinates.forEach(polygon => {
        //         polygon.forEach(ring => {
        //         ring.forEach(([x, y], i) => {
        //             const sx = xScale(x);
        //             const sy = yScale(y);
        //             if (i === 0) ctx.moveTo(sx, sy);
        //             else ctx.lineTo(sx, sy);
        //         });
        //         });
        //     });
            
        //     ctx.closePath();
        //     ctx.fillStyle = d3.interpolateViridis(contour.value); // color by threshold
        //     ctx.fill();
        //     ctx.stroke();
        // });
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