// Configuration
const API_BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '' || window.location.protocol === 'file:')
    ? 'http://localhost:5000'
    : 'https://project-samarth-7kzm.onrender.com'; // Deployed backend URL

// DOM Elements
const queryInput = document.getElementById('queryInput');
const submitBtn = document.getElementById('submitBtn');
const resultsSection = document.getElementById('results');
const answerText = document.getElementById('answerText');
const sourcesContainer = document.getElementById('sourcesContainer');
const rawData = document.getElementById('rawData');
const errorMessage = document.getElementById('errorMessage');
const loading = document.getElementById('loading');
const exampleButtons = document.querySelectorAll('.example-btn');

// Event Listeners
submitBtn.addEventListener('click', handleSubmit);
queryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        handleSubmit();
    }
});

exampleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const query = btn.getAttribute('data-query');
        queryInput.value = query;
        handleSubmit();
    });
});

// Main Submit Handler
async function handleSubmit() {
    const query = queryInput.value.trim();

    if (!query) {
        showError('Please enter a question');
        return;
    }

    // Reset UI
    hideError();
    hideResults();
    showLoading();
    disableSubmit();

    try {
        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to process query');
        }

        if (data.success) {
            displayResults(data);
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }

    } catch (error) {
        showError(`Error: ${error.message}`);
        console.error('Query error:', error);
    } finally {
        hideLoading();
        enableSubmit();
    }
}

// Display Results
function displayResults(data) {
    // Display answer
    answerText.textContent = data.answer;

    // Display sources
    if (data.sources && data.sources.length > 0) {
        sourcesContainer.innerHTML = '';
        data.sources.forEach(source => {
            const sourceItem = document.createElement('div');
            sourceItem.className = 'source-item';
            sourceItem.innerHTML = `
                <strong>${source.dataset}</strong>
                <p>📍 Region: ${source.region}</p>
                <p>📁 File: ${source.file}</p>
                ${source.period ? `<p>📅 Period: ${source.period}</p>` : ''}
                <p>${source.description}</p>
            `;
            sourcesContainer.appendChild(sourceItem);
        });
    }

    // Display raw data
    rawData.textContent = JSON.stringify(data.raw_data, null, 2);

    // Show results
    showResults();
}

// UI Helper Functions
function showResults() {
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideResults() {
    resultsSection.style.display = 'none';
}

function showLoading() {
    loading.style.display = 'block';
}

function hideLoading() {
    loading.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideError() {
    errorMessage.style.display = 'none';
}

function disableSubmit() {
    submitBtn.disabled = true;
    submitBtn.querySelector('.btn-text').style.display = 'none';
    submitBtn.querySelector('.btn-loader').style.display = 'inline';
}

function enableSubmit() {
    submitBtn.disabled = false;
    submitBtn.querySelector('.btn-text').style.display = 'inline';
    submitBtn.querySelector('.btn-loader').style.display = 'none';
}

// Check API Health on Load
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('API Status:', data);
    } catch (error) {
        console.warn('Could not connect to backend API:', error.message);
        showError('⚠️ Backend API is not reachable. Please make sure the Flask server is running.');
    }
}

// Initialize
window.addEventListener('load', () => {
    checkAPIHealth();
});
