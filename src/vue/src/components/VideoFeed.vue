<template>
    <div class="video-container">
        <!-- The <video> element displays the live camera feed to the user -->
        <video ref="videoElement" autoplay playsinline class="video-feed"></video>

        <!-- The <canvas> element is used invisibly to extract frames from the video -->
        <canvas ref="canvasElement" class="hidden-canvas"></canvas>

        <div class="controls">
            <button @click="startCamera" :disabled="isCameraActive">Start Camera</button>
            <button @click="stopCamera" :disabled="!isCameraActive">Stop Camera</button>
        </div>

        <!-- Optional: Display data received from the backend (like predictions) -->
        <div v-if="predictionResult" class="results">
            Prediction: {{ predictionResult }}
        </div>
    </div>
</template>

<script setup>
import { onUnmounted, ref } from 'vue';

// ref() is used to create reactive references to DOM elements and state variables
const videoElement = ref(null);
const canvasElement = ref(null);
const isCameraActive = ref(false);
const predictionResult = ref(null);

let stream = null;
let frameInterval = null;
// WebSocket connection placeholder
let ws = null;

// Constants for processing
const FPS = 10; // Frames per second to send to backend (lower is better for performance)
const PROCESSING_WIDTH = 320; // Downscale width before sending
const PROCESSING_HEIGHT = 240; // Downscale height before sending

// Start the camera and request permissions
const startCamera = async () => {
    try {
        // navigator.mediaDevices.getUserMedia asks the user for camera access
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user' // Prioritize the front-facing camera on mobile
            },
            audio: false // We only need video for OpenCV
        });

        // Once we have the stream, we attach it to the <video> element so the user can see it
        if (videoElement.value) {
            videoElement.value.srcObject = stream;
            isCameraActive.value = true;

            // Start the WebSocket connection and frame extraction loop
            connectWebSocket();
            startFrameExtraction();
        }
    } catch (error) {
        console.error('Error accessing the camera:', error);
        alert('Could not access the camera. Please ensure permissions are granted.');
    }
};

// Stop the camera and clean up resources
const stopCamera = () => {
    if (stream) {
        // A stream has multiple "tracks" (e.g., video, audio). We must stop all of them.
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }

    if (videoElement.value) {
        videoElement.value.srcObject = null;
    }

    isCameraActive.value = false;
    stopFrameExtraction();

    if (ws) {
        ws.close();
        ws = null;
    }
};

// Establish a WebSocket connection to your Python backend
const connectWebSocket = () => {
    // Replace this URL with your actual Python WebSocket server URL
    // Example: ws://localhost:8000/ws
    ws = new WebSocket('ws://localhost:8000/ws');

    ws.onopen = () => {
        console.log('WebSocket connection established.');
    };

    // Handle messages received FROM the Python backend (e.g., OpenCV results)
    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            // Example: If Python sends {"prediction": "Rock"}
            if (data.prediction) {
                predictionResult.value = data.prediction;
            }
        } catch (e) {
            console.error('Error parsing WebSocket message:', e);
        }
    };

    ws.onclose = () => {
        console.log('WebSocket connection closed.');
    };
};

// Extract frames from the video and send them to the backend
const startFrameExtraction = () => {
    const canvas = canvasElement.value;
    const context = canvas.getContext('2d');

    // Set the canvas size to the downscaled resolution for processing
    canvas.width = PROCESSING_WIDTH;
    canvas.height = PROCESSING_HEIGHT;

    // setInterval runs a function repeatedly at a specific interval (e.g., every 100ms for 10 FPS)
    frameInterval = setInterval(() => {
        // Only proceed if the camera is active, video is playing, and WebSocket is open
        if (!isCameraActive.value || !videoElement.value || ws?.readyState !== WebSocket.OPEN) return;

        // 1. Draw the current frame of the <video> onto the <canvas>
        // This scales the original video resolution down to the canvas dimensions
        context.drawImage(videoElement.value, 0, 0, canvas.width, canvas.height);

        // 2. Extract the image data from the canvas as a Base64 encoded JPEG string
        // The second parameter (0.7) is the JPEG quality (0.0 to 1.0) to balance size and quality
        const base64Image = canvas.toDataURL('image/jpeg', 0.7);

        // 3. Send the Base64 string to the Python backend via WebSocket
        ws.send(JSON.stringify({
            type: 'frame',
            image: base64Image
        }));

    }, 1000 / FPS);
};

// Stop the frame extraction loop
const stopFrameExtraction = () => {
    if (frameInterval) {
        clearInterval(frameInterval);
        frameInterval = null;
    }
};

// Lifecycle hook: Clean up when the component is destroyed/unmounted
// This prevents memory leaks and ensures the camera turns off if the user navigates away
onUnmounted(() => {
    stopCamera();
});
</script>

<style scoped>
.video-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
}

.video-feed {
    width: 100%;
    max-width: 640px;
    background-color: #000;
    border-radius: 8px;
    /* Mirror the video feed so it acts like a mirror for the user */
    transform: scaleX(-1);
}

/* Hide the canvas from the user, it is only for internal processing */
.hidden-canvas {
    display: none;
}

.controls {
    display: flex;
    gap: 1rem;
}

button {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    cursor: pointer;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #f8f9fa;
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.results {
    font-size: 1.5rem;
    font-weight: bold;
    color: #2c3e50;
    margin-top: 1rem;
}
</style>