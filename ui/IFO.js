// ELEMENTS

const cameraInput = document.getElementById('camera-source');

const imagePreview = document.getElementById('image-preview');
const previewImg = document.getElementById('preview-img');

const emptyState = document.getElementById('empty-state');
const loadingState = document.getElementById('loading-state');
const errorState = document.getElementById('error-state');
const errorMessage = document.getElementById('error-message');

const resultContainer = document.getElementById('result');

const prediction = document.getElementById('prediction');
const predictionDescription = document.getElementById('prediction-description');

const aircraftSection = document.getElementById('aircraft-section');
const aircraftList = document.getElementById('aircraft-list');
const aircraftCount = document.getElementById('aircraft-count');

const birdSection = document.getElementById('bird-section');
const birdList = document.getElementById('bird-list');
const birdCount = document.getElementById('bird-count');

const otherSection = document.getElementById('other-section');


// IMAGE PREVIEW

let currentImageURL = null;

function displayImage(file) {

    // Release previous image URL
    if (currentImageURL) {
        URL.revokeObjectURL(currentImageURL);
    }

    currentImageURL = URL.createObjectURL(file);

    previewImg.src = currentImageURL;
    imagePreview.classList.remove('hidden');
}


// HELPER FUNCTION

function addTextElement(parent, tagName, text, className = '') {

    const element = document.createElement(tagName);

    element.textContent = text;

    if (className) {
        element.className = className;
    }

    parent.appendChild(element);

    return element;
}


// UI STATES

function showLoading() {

    emptyState.classList.add('hidden');
    resultContainer.classList.add('hidden');
    errorState.classList.add('hidden');

    loadingState.classList.remove('hidden');
}


function showError(message) {

    loadingState.classList.add('hidden');
    emptyState.classList.add('hidden');
    resultContainer.classList.add('hidden');

    errorMessage.textContent = message;
    errorState.classList.remove('hidden');
}


// RESET RESULTS

function resetResults() {

    resultContainer.classList.add('hidden');

    aircraftSection.classList.add('hidden');
    birdSection.classList.add('hidden');
    otherSection.classList.add('hidden');

    aircraftList.replaceChildren();
    birdList.replaceChildren();
}


// PREDICTION DESCRIPTIONS

function getDescription(label) {

    const descriptions = {
        aircraft: 'Here are nearby airborne flignts.',
        bird: 'Here are the possible bird identifications.',
        other: 'The image contains a ufo...'
    };

    return descriptions[label] || 'Your image has been analyzed.';
}


// DISPLAY AIRCRAFT

function displayAircraft(flights) {

    aircraftSection.classList.remove('hidden');

    aircraftCount.textContent = flights.length;

    if (flights.length === 0) {

        addTextElement(
            aircraftList,
            'p',
            'No nearby aircraft found.',
            'no-data'
        );

        return;
    }

    flights.forEach((flight) => {

        const card = document.createElement('div');
        card.className = 'flight-card';

        addTextElement(
            card,
            'h4',
            flight.callsign || 'Unknown callsign'
        );

        addTextElement(
            card,
            'p',
            `Latitude: ${flight.latitude ?? 'Unknown'}`
        );

        addTextElement(
            card,
            'p',
            `Longitude: ${flight.longitude ?? 'Unknown'}`
        );

        addTextElement(
            card,
            'p',
            `Altitude: ${flight.altitude_ft ?? flight.altitude ?? 'Unknown'} ft`
        );

        addTextElement(
            card,
            'p',
            `Speed: ${flight.speed_mph ?? flight.speed ?? 'Unknown'} mph`
        );

        addTextElement(
            card,
            'p',
            `Category: ${flight.category ?? 'Unknown'}`
        );

        aircraftList.appendChild(card);

    });
}


// DISPLAY BIRD PREDICTIONS

function displayBirds(birds) {

    birdSection.classList.remove('hidden');

    const entries = Object.entries(birds);

    birdCount.textContent = entries.length;

    if (entries.length === 0) {

        addTextElement(
            birdList,
            'p',
            'No bird predictions available.',
            'no-data'
        );

        return;
    }

    entries.forEach(([name, confidence]) => {

        const card = document.createElement('div');
        card.className = 'bird-card';

        const top = document.createElement('div');
        top.className = 'bird-card-top';

        addTextElement(top, 'span', name);

        const percentage = Number(confidence);

        addTextElement(
            top,
            'span',
            `${percentage.toFixed(1)}%`,
            'bird-confidence'
        );

        card.appendChild(top);

        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';

        const progressFill = document.createElement('div');
        progressFill.className = 'progress-fill';

        // Keep percentage between 0 and 100
        progressFill.style.width =
            `${Math.min(100, Math.max(0, percentage))}%`;

        progressBar.appendChild(progressFill);
        card.appendChild(progressBar);

        birdList.appendChild(card);

    });
}


// RENDER RESULTS

function renderResult(data) {

    resetResults();

    loadingState.classList.add('hidden');
    emptyState.classList.add('hidden');

    resultContainer.classList.remove('hidden');

    // Display prediction
    prediction.textContent = data.birdorplane;

    predictionDescription.textContent =
        getDescription(data.birdorplane);

    // Aircraft
    if (data.birdorplane === 'aircraft') {

        const flights = data.nearby_aircraft || [];

        displayAircraft(flights);

    }

    // Bird
    else if (data.birdorplane === 'bird') {

        const birds = data.bird_predictions || {};

        displayBirds(birds);

    }

    // Other
    else {

        otherSection.classList.remove('hidden');

        otherSection.querySelector('p').textContent =
            data.message || 'No bird or aircraft was identified.';

    }

}


// IMAGE UPLOAD AND BACKEND REQUEST

cameraInput.addEventListener('change', async (event) => {

    const file = event.target.files[0];

    if (!file) return;

    // Validate image
    if (!file.type.startsWith('image/')) {

        showError('Please upload a valid image file.');

        cameraInput.value = '';

        return;
    }

    // Display image immediately
    displayImage(file);

    // Reset old results
    resetResults();

    // Show loading screen
    showLoading();

    // Prepare image for Flask
    const formData = new FormData();

    formData.append('image', file);

    try {

        // Send image to Flask
        const response = await fetch(
            'http://127.0.0.1:5000/upload',
            {
                method: 'POST',
                body: formData
            }
        );

        // Read JSON response
        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.error || `Server returned ${response.status}`
            );

        }

        // Display results
        renderResult(data);

    }

    catch (error) {

        console.error('Upload error:', error);

        showError(error.message);

    }

    finally {

        // Allow the same image to be selected again
        cameraInput.value = '';

    }

});