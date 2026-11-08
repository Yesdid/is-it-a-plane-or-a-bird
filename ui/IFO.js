const fileInput = document.getElementById('file-upload');
const resultContainer = document.getElementById('result');
const videoElement = document.getElementById('webcam');

function showMessage(html) {
    resultContainer.innerHTML = html;
}

async function uploadImage(file) {
    const formData = new FormData();
    formData.append('image', file);

    const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error(`Server returned ${response.status}: ${response.statusText}`);
    }

    return response.json();
}

function showPrediction(data) {
    showMessage(`<strong>Prediction:</strong> ${data.birdorplane}`);
}

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480 },
            audio: false
        });
        videoElement.srcObject = stream;
    } catch (error) {
        console.error('Error accessing the camera: ', error);
        showMessage('<strong>Error:</strong> Camera access was denied or is not available.');
    }
}

fileInput.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    showMessage('<p>Uploading and processing...</p>');

    try {
        const data = await uploadImage(file);
        showPrediction(data);
    } catch (error) {
        console.error('Upload error:', error);
        showMessage(`<strong>Error:</strong> ${error.message}`);
    }
});

startCamera();