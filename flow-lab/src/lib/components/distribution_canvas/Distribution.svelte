<script lang="ts">
    import * as d3 from 'd3';
    import * as tf from '@tensorflow/tfjs';
    import katex from 'katex';
    import 'katex/dist/katex.min.css';

    import { interfaceSettings } from '$lib/state';
    import { UIState } from '$lib/state';
    
    // export let currentTime: number = 0.0; // Default value for the time
    // export let isPlaying: boolean = false; // Flag to indicate if the animation is playing
    // export let targetDistributionSamples = tf.tensor([]); // Number of samples to generate
    // export let sourceDistributionSamples = tf.tensor([]); // Number of samples to generate
    // export let currentDistributionSamples = tf.tensor([]); // Number of samples to generate
    export let data: tf.Tensor; // Data to plot
    export let xLocation: number = 0; // X location of the contour
    export let opacity: number = 0.5; // Opacity of the contour
    export let labelIsLatex: boolean = false; // Flag to indicate if the label is in LaTeX format
    export let svgElement: SVGSVGElement;
    export let label: string; // Label for the distribution
    export let distributionId: string; // ID for the distribution canvas
    export let displayMode: string = "heatmap"; // Display mode for the distribution

    function plotContour(
        data: tf.Tensor,
        opacity: number = 0.5,
        xLocation: number = 0,
        distributionId: string = "target",
    ) {
        // Convert data to plain 2d array
        let values = data.arraySync() as number[][];
        // 2. Build histogram
        const xScale = d3.scaleLinear().domain([$UIState.domainRange.xMin, $UIState.domainRange.xMax]).range([0, interfaceSettings.distributionWidth]);
        const yScale = d3.scaleLinear().domain([$UIState.domainRange.yMin, $UIState.domainRange.yMax]).range([0, interfaceSettings.distributionHeight]);

        const contours = d3.contourDensity()
            .x(d => xScale(d[0]))
            .y(d => yScale(d[1]))
            .size([interfaceSettings.distributionWidth, interfaceSettings.distributionHeight])
            .bandwidth(30)
            .thresholds(5)
            (values)

        // 4. Scales for drawing
        const svg = d3.select("svg"); 
        // Select the group by ID, or create if not exists
        // NOTE: This prevents unwanted recreation of the group
        let group = svg.select(`#${distributionId}`);
        if (group.empty()) {
            group = svg.append("g").attr("id", distributionId);
        } else {
            group.selectAll("*").remove(); // Clear previous contents of this group
        }
        // Prepare a color palette
        const color = d3.scaleSequential(d3.interpolateBlues)
            .domain([0, d3.max(contours, d => d.value) * 1.4]);
        // 5. Draw contours
        group.selectAll("path")
            .data(contours)
            .enter()
            .append("path")
            .attr("d", d3.geoPath())
            .attr("fill", d => color(d.value))
            .attr("stroke", "#000")
            .attr("stroke-width", 2)
            .attr("stroke-opacity", opacity)
            .attr("fill-opacity", opacity)
            .attr("transform", `translate(${xLocation}, 0)`);
    }

    function plotHeatmap(
        data: tf.Tensor,
        opacity: number = 0.5,
        xLocation: number = 0,
        distributionId: string = "target",
    ) {
        const values = data.arraySync() as number[][];

        // Extract range from UIState
        const xDomain = [$UIState.domainRange.xMin, $UIState.domainRange.xMax];
        const yDomain = [$UIState.domainRange.yMin, $UIState.domainRange.yMax];

        const width = interfaceSettings.distributionWidth;
        const height = interfaceSettings.distributionHeight;

        const xScale = d3.scaleLinear().domain(xDomain).range([0, width]);
        const yScale = d3.scaleLinear().domain(yDomain).range([0, height]);

        const xBins = 60;
        const yBins = 60;
        const xStep = (xDomain[1] - xDomain[0]) / xBins;
        const yStep = (yDomain[1] - yDomain[0]) / yBins;

        // Initialize grid counts
        const grid = Array.from({ length: xBins }, () =>
            Array.from({ length: yBins }, () => 0)
        );

        // Fill grid with counts
        for (const [x, y] of values) {
            const xi = Math.floor((x - xDomain[0]) / xStep);
            const yi = Math.floor((y - yDomain[0]) / yStep);
            if (xi >= 0 && xi < xBins && yi >= 0 && yi < yBins) {
                grid[xi][yi]++;
            }
        }

        const flatGrid = grid.flat();
        const maxDensity = d3.max(flatGrid);

        const color = d3.scaleSequential(d3.interpolateInferno)
            .domain([0, maxDensity]);

        const svg = d3.select("svg");

        let group = svg.select(`#${distributionId}`);
        if (group.empty()) {
            group = svg.append("g").attr("id", distributionId);
        } else {
            group.selectAll("*").remove();
        }

        // Render cells
        for (let xi = 0; xi < xBins; xi++) {
            for (let yi = 0; yi < yBins; yi++) {
                group.append("rect")
                    .attr("x", xScale(xDomain[0] + xi * xStep) + xLocation)
                    .attr("y", yScale(yDomain[0] + yi * yStep))
                    .attr("width", xScale(xDomain[0] + xStep) - xScale(xDomain[0]))
                    .attr("height", yScale(yDomain[0] + yStep) - yScale(yDomain[0]))
                    .attr("fill", color(grid[xi][yi]))
                    .attr("fill-opacity", opacity)
                    .attr("stroke", "none");
            }
        }
    }

    function plotScatterPlot(
        data: tf.Tensor,
        opacity: number = 0.5,
        xLocation: number = 0,
        distributionId: string = "target",
        maximumPoints: number = 1000,
    ) {
        // Convert data to plain 2d array
        data = data.arraySync() as number[][];
        // If the data is too large, sample it down to a smaller size
        data = data.slice(0, Math.min(data.length, maximumPoints));
        // Comptue the range of the data
        let xMin = d3.min(data, d => d[0]);
        let xMax = d3.max(data, d => d[0]);
        let yMin = d3.min(data, d => d[1]);
        let yMax = d3.max(data, d => d[1]);
        const margin = 0.1;
        const xRange = xMax - xMin;
        const yRange = yMax - yMin;
        xMin -= margin * xRange;
        xMax += margin * xRange;
        yMin -= margin * yRange;
        yMax += margin * yRange;

        const xScale = d3.scaleLinear().domain([xMin, xMax]).range([0, interfaceSettings.distributionWidth]);
        const yScale = d3.scaleLinear().domain([yMin, yMax]).range([0, interfaceSettings.distributionHeight]);

        // Make a scatter plot
        const svg = d3.select("svg");
        // Select the group by ID, or create if not exists
        // NOTE: This prevents unwanted recreation of the group
        let group = svg.select(`#${distributionId}`);
        if (group.empty()) {
            group = svg.append("g").attr("id", distributionId);
        } else {
            group.selectAll("*").remove(); // Clear previous contents of this group
        }
        
        // Draw the points
        group.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", d => xScale(d[0]))
            .attr("cy", d => yScale(d[1]))
            .attr("r", 3)
            .attr("opacity", opacity)
            .attr("fill", interfaceSettings.pointColor)
            .attr("transform", `translate(${xLocation}, 0)`);
    }

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

    // Update the contour map data if the data changes
    $: if (data && svgElement) {
        // Plot the distribution
        if (displayMode === "scatter") {
            // Plot the scatter plot
            plotScatterPlot(data, opacity, xLocation, distributionId);
        } else if (displayMode === "heatmap") {
            // Plot the contour
            plotHeatmap(data, opacity, xLocation, distributionId);
        } else if (displayMode === "contour") {
            // Plot the contour
            plotContour(data, opacity, xLocation, distributionId);
        } else {
            console.error("Unknown display mode: ", displayMode);
        }
        // Plot title above the contour
        // TODO change manual text display location maybe
        if (!labelIsLatex) {
            displayText(label, xLocation + interfaceSettings.distributionWidth / 2, 50, distributionId);
        } else {
            // Create a foreignObject to hold HTML
            displayLatex(label, xLocation, 50 - 52, distributionId);
        }
    }
</script>

<style>
</style>
