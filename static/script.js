const chatContainer = document.getElementById('chat-container');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

let history = [];

function addMessage(content, role) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    // Simple markdown parsing for bold and newlines
    let formattedContent = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');

    bubble.innerHTML = formattedContent;

    messageDiv.appendChild(bubble);
    chatContainer.appendChild(messageDiv);

    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Update history
    history.push({ role, content });
}

function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant loading-message';
    loadingDiv.innerHTML = `
        <div class="typing-indicator">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
    `;
    chatContainer.appendChild(loadingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return loadingDiv;
}

function removeLoading(loadingDiv) {
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = userInput.value.trim();
    if (!message) return;

    // Clear input
    userInput.value = '';

    // Add user message
    addMessage(message, 'user');

    // Show loading
    const loadingDiv = showLoading();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                history: history.slice(0, -1) // Send history excluding the just added message to avoid duplication if logic changes, but actually backend handles it.
                // Wait, backend expects history + current message.
                // My backend logic:
                // messages = [history] + [current_message]
                // So I should send history excluding the current one, and current one as 'message'.
                // But I just pushed current one to history.
                // So I should slice it.
            })
        });

        const data = await response.json();

        removeLoading(loadingDiv);

        if (data.error) {
            addMessage(`Error: ${data.error}`, 'assistant');
        } else {
            addMessage(data.response, 'assistant');
        }

    } catch (error) {
        removeLoading(loadingDiv);
        addMessage(`Error: ${error.message}`, 'assistant');
    }
});
