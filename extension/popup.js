const urlDisplay = document.getElementById('url-display');
const promptInput = document.getElementById('prompt-input');
const sendButton = document.getElementById('send-button');
const responseArea = document.getElementById('response-area');

let activeTabUrl = '';

// Function to get the active tab's URL when the popup is opened
document.addEventListener('DOMContentLoaded', () => {
    // This is a Chrome Extension API call
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        if (tabs[0] && tabs[0].url && tabs[0].url.startsWith('http')) {
            activeTabUrl = tabs[0].url;
            urlDisplay.textContent = activeTabUrl;
        } else {
            urlDisplay.textContent = "Cannot get URL. Try a valid website.";
            sendButton.disabled = true; // Disable sending if URL is invalid
        }
    });
});

// Add a click listener to the send button
sendButton.addEventListener('click', sendDataToBackend);

async function sendDataToBackend() {
    const prompt = promptInput.value.trim();

    if (!prompt) {
        responseArea.textContent = "Please enter a prompt.";
        return;
    }
    if (!activeTabUrl) {
        responseArea.textContent = "Could not find a valid page URL to process.";
        return;
    }

    // Provide visual feedback
    sendButton.disabled = true;
    responseArea.textContent = "Sending data... Please wait.";

    try {
        // Send BOTH the URL and the prompt to the Python backend
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: activeTabUrl,
                prompt: prompt
            })
        });

        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }

        const data = await response.json();
        responseArea.textContent = data.response;

    } catch (error) {
        console.error("Error communicating with backend:", error);
        responseArea.textContent = "Error: Could not connect to the backend. Is the Python server running?";
    } finally {
        // Re-enable the button after the request is complete
        sendButton.disabled = false;
    }
}
