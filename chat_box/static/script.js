document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-prompt').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
    const userPrompt = document.getElementById('user-prompt').value.trim();
    if (!userPrompt) return;

    const chatHistory = document.getElementById('chat-history');
    chatHistory.innerHTML += `<div class="chat-message user-message">${sanitizeHTML(userPrompt)}</div>`;
    document.getElementById('user-prompt').value = '';

    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: userPrompt })
    });

    const data = await response.json();
    if (data.response) {
        chatHistory.innerHTML += `<div class="chat-message bot-message">${sanitizeHTML(data.response)}</div>`;
    } else {
        chatHistory.innerHTML += `<div class="chat-message bot-message">Error: ${data.error || "Unable to process your request."}</div>`;
    }

    chatHistory.scrollTop = chatHistory.scrollHeight; // Auto-scroll
}

function sanitizeHTML(str) {
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML.replace(/\n/g, '<br>'); // Preserve line breaks
}
