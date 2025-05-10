/*
*    Web worker that runs sampling for a given model. 
*/ 
// import * as tf from '@tensorflow/tfjs';
// import '@tensorflow/tfjs-backend-wasm';

// tf.setBackend('wasm').then(() => {
//   self.postMessage({ status: 'ready' });
// });

self.onmessage = async (e) => {
    const { type, data } = e.data;

    if (type === 'sample') {
        // Load up a model from the given file path
        // Run sampling with the model based on data.numberOfSteps and data.numSamples
        // Return the samples to the main thread
        console.log("Running sampler worker.")
        // const input = tf.tensor(data.input);
        // console.log("Do worker model behavior. ")
        // // const output = input.square(); // replace with your real model
        // const result = await output.array();
        self.postMessage({ type: 'result', data: "result" });
    }
};
