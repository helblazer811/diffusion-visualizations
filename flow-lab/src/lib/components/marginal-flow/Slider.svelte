<script lang="ts">
    export let value: number;
</script>

<style>
    .marginal-flow-slider {
        width: 100%;
    }

    .marginal-flow-slider input[type="range"] {
        width: 100%;
        height: 40px;
        background: #ddd;
        border-radius: 5px;
        outline: none;
    }

    .label-container {
        font-size: 1.3em;
        color:#2e2e2e;
        position: relative;
        width: 100%;
        height: 20px;
        margin-top: 4px;
    }

    .slider-labels {
        display: flex;
        justify-content: space-between;
        padding: 0 4px;
    }

    .center-label {
        position: absolute;
        left: 50%;
        top: 0;
        transform: translateX(-50%);
    }
</style>

<div class="marginal-flow-slider">
    <input 
        type="range" 
        min="0" 
        max="1" 
        step="0.01"
        bind:value
    />
    <div class="label-container">
        <div class="slider-labels">
            <span>t = 0</span>
            <span>t = 1</span>
        </div>
        <div class="center-label">Time</div>
    </div>
</div>
