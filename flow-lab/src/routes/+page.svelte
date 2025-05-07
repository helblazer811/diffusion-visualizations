<script>
    import MarginalFlow from '$lib/components/marginal-flow/MarginalFlow.svelte';
</script>

<style>
    .heading {
        text-align: center;
        margin: 0 auto; /* Center the div horizontally */
        color: #494949;
        font-family: Helvetica, sans-serif;
    }

    .heading h1 {
        font-size: 4em;
        margin: 10px;
    }

    .heading h2 {
        font-size: 2.5em;
        margin: 0;
    }

</style>

<div class="heading">
    <h1>Flow Matching</h1>
    <h2>The Evolution of the Marginal Probability Path</h2>
</div>
<MarginalFlow />