<script>
    import * as tf from '@tensorflow/tfjs';
    import { onMount } from 'svelte';
    // Load up the application config
    import { pretrainedModelPaths, modelTypeToModelClass, modelConfig, datasetNameToPath, trainingConfig} from '$lib/config';
    // Load up the application state
    import { UIState, model } from '$lib/state';
    // Load up the components
    import TimeSlider from '$lib/components/TimeSlider.svelte';
    import TrainingBar from '$lib/components/TrainingBar.svelte';
    import DistributionCanvas from '$lib/components/distribution_canvas/DistributionCanvas.svelte';

    onMount(async () => {
        // Load up the default cached model
        // const defaultModelType = UIState.get("modelType");
        // const defaultModelPath = pretrainedModelPaths[defaultModelType];
        // Train default model type
        const defaultModelType = $UIState.modelType;
        const modelClass = modelTypeToModelClass[defaultModelType];
        // Initialize the model
        const ourModel = new modelClass(
            modelConfig[defaultModelType]["dim"],
            modelConfig[defaultModelType]["hidden"],
        );
        // Load up the chosen training dataset points as tf tensor
        const trainingDatasetPath = datasetNameToPath[$UIState.datasetName];
        const response = await fetch(trainingDatasetPath);
        const data = await response.json();
        const pointsTensor = tf.tensor(data.points); // Convert the data to a tensor
        // Train the model
        ourModel.train(
            pointsTensor,
            trainingConfig["iterations"],
            trainingConfig["batchSize"],
        ).then(() => {
            console.log('Model trained successfully');
            // Save the model into the model store
            model.set(ourModel);
            // Save the model to the specified path
            // model.save(defaultModelPath);
        }).catch((error) => {
            console.error('Error training the model:', error);
        });
    });

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
        <DistributionCanvas />  
        <TimeSlider /> 
        <!-- <DatasetMenu />  Dataset selector menu to choose the dataset to train on -->
    </div>
</div>