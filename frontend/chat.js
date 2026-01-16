const chatHistory = document.getElementById('chat-history');
const buttonContainer = document.getElementById('button-container');
const textInputForm = document.getElementById('text-input-form');
const userInput = document.getElementById('user-input');
const cancelTextModeBtn = document.getElementById('cancel-text-mode');

const API_URL = 'http://127.0.0.1:8001';

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    fetchButtons('init');
});

async function fetchButtons(type) {
    try {
        const response = await fetch(`${API_URL}/init`);
        const data = await response.json();
        renderButtons(data.buttons);
    } catch (error) {
        addMessage("Failed to connect to server.", 'bot');
    }
}

async function sendMessage(message, isButton = false, value = null) {
    // 1. Add User Message
    addMessage(message, 'user');

    // 2. Clear input
    userInput.value = '';

    // 3. Show loading state (optional)

    // 4. Send to Backend
    try {
        const payload = value ? value : message; // send value code if it's a button, else text

        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: payload })
        });

        const data = await response.json();

        // 5. Render Bot Response
        if (data.text) {
            addMessage(data.text, 'bot');
        }

        // 6. Render Buttons if any
        if (data.buttons && data.buttons.length > 0) {
            renderButtons(data.buttons);
            // Hide text input if we are back to buttons, unless specific button type
            const hasModeSwitch = data.buttons.some(b => b.type === 'mode_switch');
            if (!hasModeSwitch) {
                // If we are navigating categories, stay in button mode
                toggleInputMode(false);
            }
        }
    } catch (error) {
        addMessage("Sorry, something went wrong.", 'bot');
        console.error(error);
    }
}

function renderButtons(buttons) {
    buttonContainer.innerHTML = '';

    buttons.forEach(btn => {
        const button = document.createElement('button');
        button.className = 'chat-btn';
        button.textContent = btn.label;

        button.onclick = () => {
            if (btn.type === 'mode_switch') {
                // Switch to text input
                toggleInputMode(true);
            } else {
                // Send selection as a message
                sendMessage(btn.label, true, btn.value);
            }
        };

        buttonContainer.appendChild(button);
    });
}

function toggleInputMode(showText) {
    if (showText) {
        buttonContainer.classList.add('hidden');
        textInputForm.classList.remove('hidden');
        cancelTextModeBtn.classList.remove('hidden');
        userInput.focus();
    } else {
        buttonContainer.classList.remove('hidden');
        textInputForm.classList.add('hidden');
        cancelTextModeBtn.classList.add('hidden');
    }
}

// Handle Form Submit
textInputForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (userInput.value.trim()) {
        sendMessage(userInput.value.trim());
    }
});

// Handle Cancel Text Mode
cancelTextModeBtn.addEventListener('click', () => {
    toggleInputMode(false);
    // Optionally re-fetch init buttons or just go back to last view
    sendMessage("Main Menu", true, "init");
});


function addMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `message ${sender}-message`;
    // Simple markdown parsing for links
    // Replace [Link Text](url) with <a href="url">Link Text</a>
    const htmlText = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
        .replace(/\n/g, '<br>');
    div.innerHTML = htmlText;

    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}
