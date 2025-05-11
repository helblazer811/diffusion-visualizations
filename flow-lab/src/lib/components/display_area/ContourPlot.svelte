
<script lang="ts">
    import * as tf from '@tensorflow/tfjs';
    import * as d3 from 'd3';

    import { interfaceSettings, UIState } from '$lib/state';

    export let data: tf.Tensor; // Data to plot
    export let distributionId: string = "target"; // ID for the distribution canvas
    export let xLocation: number = 0; // X location of the contour
    export let opacity: number = 0.5; // Opacity of the contour
    export let colorMap: string = "Blues"; // Color map for the heatmap
    export let bandwidth: number = 20; // Bandwidth for the contour density

    let svgElement: SVGSVGElement; // Create a separate SVG element for each distribution

    let colorScale = d3[`interpolate${colorMap}`];
    
    function plotContour(
        data: tf.Tensor,
        opacity: number = 0.5,
        xLocation: number = 0,
        distributionId: string = "target",
        numberOfContours: number = 10,
        showBorder: boolean = true,
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
            .thresholds(numberOfContours)
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
        const color = d3.scaleSequential(colorScale)
            .domain([0, d3.max(contours, d => d.value) * 1.2]);
        // 5. Draw contours
        group.selectAll("path")
            .data(contours)
            .enter()
            .append("path")
            .attr("d", d3.geoPath())
            .attr("fill", d => color(d.value))
            .attr("stroke", "#ccc")
            .attr("stroke-width", showBorder ? 2 : 0)
            .attr("stroke-opacity", opacity)
            .attr("fill-opacity", opacity)
            .attr("transform", `translate(${xLocation}, 0)`);
    }

    // If the data points change then replot
    $: if (data && svgElement) {
        plotContour(data, opacity, xLocation, distributionId);
    }
</script>

<style> 
    svg {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
</style>

<svg
    bind:this={svgElement}
    id="svg_{distributionId}" 
    width={interfaceSettings.distributionWidth}
    height={interfaceSettings.distributionHeight}
    style={"left: " + xLocation + "px;"}
>
</svg>