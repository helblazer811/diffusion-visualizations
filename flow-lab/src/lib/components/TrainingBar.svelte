<script>
    import HyperparameterSelect from '$lib/components/HyperparameterSelect.svelte';
    import { hyperparameterMenuConfig } from '$lib/state';

</script>

<style>
    .training-bar {
        height: 110px;
        width: 100%;
        background-color: white;
        /* Add drop shadow on bottom */
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
    }

    .training-bar-inner-container {
        display: flex;
        width: 1400px;
        align-items: center;
        height: 100%;
        width: var(--inner-component-width);
        margin: 0 auto;
    }  

    .hyperparameter-menu {
        display: flex;
        /* margin-left: 20px; */
        flex-direction: row;
    }
</style>

<div class="training-bar">
    <div class="training-bar-inner-container">
        <div class="hyperparameter-menu">
            {#each Object.entries(hyperparameterMenuConfig) as [name, entry]}
                <HyperparameterSelect entry={entry} />
            {/each}
        </div>
    </div>
</div>