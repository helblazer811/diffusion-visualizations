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
        // Plot the target distribution
        plotContour(data, opacity, xLocation, distributionId);
        // Plot title above the contour
        // TODO change manual text display location maybe
        if (!labelIsLatex) {
            displayText(label, xLocation + interfaceSettings.distributionWidth / 2, 50, distributionId);
        } else {
            // Create a foreignObject to hold HTML
            displayLatex(label, xLocation, 50 - 52, distributionId);
        }
    }
    // // Update source distribution if it changes
    // $: if (UIState.sourceDistributionSamples) {
    //     // Plot the source distribution
    //     plotContour(UIState.sourceDistributionSamples, 0.15, 0);
    //     // Plot title above the contour
    //     const svg = d3.select(svgElement);
    //     displayText(svg, "Source Distribution", 0 + interfaceSettings.distributionWidth / 2, 50);
    // }
    // // Update current distribution if it changes
    // $: if (UIState.currentDistributionSamples) {
    //     const xLocation = UIState.currentTime * (interfaceSettings.distributionWidth - 800);
    //     plotContour(UIState.currentDistributionSamples, 1.0, xLocation);
    //     // Only show if the x location is not overlapping with source or target
    //     if (xLocation > 150 && xLocation < interfaceSettings.distributionWidth - 800 - 150) {
    //         displayLatex("p_t(x)", xLocation + 800 / 2 - 150, 50 - 52);
    //     }
    // }
    // // Run the plot contour if current Distribution changes
    // $: if (
    //     UIState.targetDistributionSamples && svgElement || 
    //     UIState.currentDistributionSamples && svgElement
    // ) {
    //     // Clear existing contours
    //     const svg = d3.select(svgElement);
    //     svg.selectAll("*").remove(); // Clear previous contours
    //     // Plot the source distribution
    //     plotContour(UIState.currentDistributionSamples, 0.15, 0);
    //     // Plot the target distribution
    //     // plotContour(UIState.targetDistributionSamples, 0.15, 800);
    //     // // Plot title above the contour
    //     // svg.append("text")
    //     //     .attr("x", 800 + distributionWidth / 2)
    //     //     .attr("y", 50)
    //     //     .attr("text-anchor", "middle")
    //     //     .style("font-size", "34px")
    //     //     .style("font-family", "Helvetica, sans-serif")
    //     //     .style("fill", "#7b7b7b")
    //     //     .text("Target Distribution");
    //     // // Plot the current distribution
    //     // // First compute the x location based on the current time
    //     // const xLocation = currentTime * (distributionCanvasWidth - distributionWidth);
    //     // plotContour(currentDistributionSamples, 1.0, xLocation);
    //     // // Draw latex over current distribution
    //     // // Only show if the x location is not overlapping with source or target
    //     // if (xLocation > 150 && xLocation < distributionCanvasWidth - distributionWidth - 150) {
    //     //     // Create a foreignObject to hold HTML
    //     //     displayLatex("p_t(x)", xLocation + distributionWidth / 2 - 150, 50 - 52);
    //     // }
</script>

<style>
    /* .canvas {
        width: 100%;
        height: 100%;
        background-color: var(--light-gray);
    } */
</style>

<!-- <div class="canvas"> -->
<!-- <canvas id="densityCanvas" bind:this={canvas} width="0" height="0"></canvas> -->
<!-- <svg bind:this={svgElement} width={interfaceSettings.distributionCanvasWidth} height={canvasHeight}></svg>    -->
<!-- </div> -->