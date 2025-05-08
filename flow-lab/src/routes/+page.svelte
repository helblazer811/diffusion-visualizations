<script>
    import TrainingBar from '$lib/components/TrainingBar.svelte';
    // import Canvas from '$lib/components/Canvas.svelte';
</script>

<style>
    .sub-title-container {
        height: 70px;
        width: 100%;
        background-color: var(--dark-blue);
        display: flex;
        justify-content: center;
        align-items: center;
        /* max-width: var(--inner-component-width); */
        margin: 0 auto;
    }

    .sub-title-inner-container {
        display: flex;
        align-items: center;
        height: 100%;
        width: var(--inner-component-width);
    }

    .sub-title {
        margin: 0;
        font-size: 1.5em;
        color: white;
        font-family: var(--font-family);
        font-weight: 200; /* Thin font */
    }

    .main-area {
        background-color: var(--light-gray);
        height: 800px;
    }

</style>

<div class="container">
    <div class="sub-title-container">
        <div class="sub-title-inner-container">
            <h1 class="sub-title">Learn about diffusion and flow based generative models with interactive visualization. </h1>
        </div>
    </div>
    <TrainingBar />
    <div class="main-area">
        <!-- <DisplayOptionsMenu />  Menu of items to choose to collect from -->
        <!-- <Canvas />  Canvas to the d3 animations like the flows, trajectories, source and target distribution -->
        <!-- <DatasetMenu />  Dataset selector menu to choose the dataset to train on -->
    </div>
</div>