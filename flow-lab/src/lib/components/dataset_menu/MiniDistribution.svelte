
<script lang="ts"> 
    import * as d3 from 'd3';
    import {interfaceSettings, UIState } from '$lib/state';

    export let data; // Data to plot
    export let distributionId = "target"; // ID for the distribution canvas

    let svgElement: SVGSVGElement; // Create a separate SVG element for each distribution

    function handleClick(){
        console.log("Clicked on distribution: ", distributionId);
        // Change this dataset to be the current one
        UIState.update(state => ({
            ...state,
            datasetName: distributionId,
        }));
    }

    async function plotPoints(
        data: tf.Tensor, // Data to plot
        distributionId: string = "target", // ID for the distribution canvas
    ){
        // Replace distributionId spaces with underscores
        const replacedDistributionId = distributionId.replace(/\s+/g, '_');
        // Convert data to plain 2d array
        data = await data.arraySync() as number[][];
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
        console.log("xMin: ", xMin);
        console.log("xMax: ", xMax);
        console.log(data)
        const xScale = d3.scaleLinear().domain([xMin, xMax]).range([0, 65]);
        const yScale = d3.scaleLinear().domain([yMin, yMax]).range([0, 65]);
        // Make a scatter plot
        const svg = d3.select(svgElement); 
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
            .attr("r", 1)
            .attr("fill", interfaceSettings.pointColor);
    }

    // If data changes, replot the points
    $: if (data && svgElement) {
        console.log("Plotting points");
        console.log(data.shape)
        plotPoints(data, distributionId);
    }

</script>

<style>
    .mini-distribution {
        width: 65px;
        height: 65px;
        border: 2px solid #9f9f9f;
        position: relative;
        /* Rounded corners */
        border-radius: 5px;
        margin-left: 20px;
    }

    svg {
        width: 100%;
        height: 100%;
    }

</style>

<div class="mini-distribution" on:click={handleClick}>
    <svg 
        bind:this={svgElement}
        id="{distributionId}"
    ></svg>
</div>