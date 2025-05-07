<script lang="ts">
    export let value: number;
</script>

<style>
    .marginal-flow-slider {
        /* width: 100%; */
        height: 40px;
        /* Add padding of half the width of the frame to each side 300px */
        padding: 0 200px;
    }

    .slider {
        -webkit-appearance: none;
        width: 100%;
        height: 8px; /* match the thumb size */
        border-radius: 5px;
        background: #d3d3d3;
        outline: none;
        display: block;       /* ensure block display */
        margin: 0 auto;       /* center horizontally */
        position: relative;   /* helps with alignment */
        top: 0;               /* reset any browser default offset */
    }

    .slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background: #4594e3;
        cursor: pointer;
    }

    .slider::-moz-range-thumb {
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background: #4594e3;
        cursor: pointer;
    }

    .label-container {
        font-size: 1.3em;
        color:#2e2e2e;
        position: relative;
        width: 100%;
        /* height: 10px; */
        /* margin-top: 4x; */
    }

    .tick-container {
        position: relative;
        width: 100%;
        height: 20px;
        margin-top: 4px;
    }

    .tick {
        position: absolute;
        top: 0;
        width: 3px;
        height: 12px;
        background-color: #7b7b7b;
    }

    .tick-label {
        position: absolute;
        top: 15px;
        font-size: 2.0em;
        transform: translateX(-50%);
        font-family: Helvetica, sans-serif;
        color: #7b7b7b;
    }

</style>

<div class="marginal-flow-slider">
    <input 
        type="range" 
        min="0" 
        max="1" 
        step="0.01"
        list="ticks"
        class="slider"
        bind:value
    />
    <div class="tick-container">
        <div class="tick" style="left: 1%;"></div>
        <div 
            class="tick-label" 
            style="left: 1.2%;"
        >
            0
        </div>
        <div class="tick" style="left: 99%;"></div>
        <div 
            class="tick-label" 
            style="left: 99.1%;"
        >
            1
        </div>
        <div class="tick-label" style="left: 49%;">
            Time
        </div>
    </div>
</div>
