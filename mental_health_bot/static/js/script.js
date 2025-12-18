function sendMessage() {
    const input = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const message = input.value.trim();

    if (message) {
        // Disable input and button while sending
        input.disabled = true;
        sendBtn.disabled = true;
        const originalBtnContent = sendBtn.innerHTML;
        sendBtn.innerHTML = '<div class="spinner"></div>'; // You might need CSS for a spinner, or just ...
        sendBtn.innerHTML = `
            <svg class="animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" style="animation: spin 1s linear infinite; width: 20px; height: 20px;">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
        `;

        addMessage(message, 'user');
        input.value = '';

        // Add typing indicator
        const typingId = showTypingIndicator();

        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message
            }),
        })
            .then(response => response.json())
            .then(data => {
                removeTypingIndicator(typingId);
                addMessage(data.response, 'bot');

                if (data.resources && data.resources.length > 0) {
                    const resourceHtml = data.resources.map(res =>
                        `<div class="resource-card">
                        <div style="font-weight: 500; color: #34d399; margin-bottom: 4px;">Recommended:</div>
                        <div style="color: var(--text-primary); margin-bottom: 8px;">${res.title}</div>
                        <a href="${res.url}" target="_blank">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16">
                                <path d="M10 16.5l6-4.5-6-4.5v9zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
                            </svg>
                            Watch Video
                        </a>
                    </div>`
                    ).join('');

                    const chatBox = document.getElementById('chat-box');
                    const resourceDiv = document.createElement('div');
                    resourceDiv.className = 'message bot-message';
                    resourceDiv.innerHTML = "I found some resources that might help:<br>" + resourceHtml;
                    chatBox.appendChild(resourceDiv);
                    scrollToBottom();
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                removeTypingIndicator(typingId);
                addMessage("Sorry, I'm having trouble connecting right now.", 'bot');
            })
            .finally(() => {
                // Re-enable input
                input.disabled = false;
                sendBtn.disabled = false;
                sendBtn.innerHTML = originalBtnContent;
                input.focus();
            });
    }
}

function addMessage(text, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = text.replace(/\n/g, '<br>');
    chatBox.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const chatBox = document.getElementById('chat-box');
    const id = 'typing-' + Date.now();
    const indicator = document.createElement('div');
    indicator.className = 'message bot-message typing-indicator';
    indicator.id = id;
    indicator.style.display = 'block'; // Override default none if set in CSS
    indicator.innerHTML = `
        <span style="display: inline-block; width: 24px;">
            <svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <style>
                    .spinner_b2T7{animation:spinner_xe7Q .8s linear infinite}.spinner_YRVV{animation-delay:-.65s}.spinner_c9oY{animation-delay:-.5s}@keyframes spinner_xe7Q{93.75%,100%{r:3px}46.875%{r:.2px}}
                </style>
                <circle class="spinner_b2T7" cx="4" cy="12" r="3" fill="#ffffff"/>
                <circle class="spinner_b2T7 spinner_YRVV" cx="12" cy="12" r="3" fill="#ffffff"/>
                <circle class="spinner_b2T7 spinner_c9oY" cx="20" cy="12" r="3" fill="#ffffff"/>
            </svg>
        </span>
    `;
    chatBox.appendChild(indicator);
    scrollToBottom();
    return id;
}

function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

function scrollToBottom() {
    const chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Allow Enter key to submit
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function triggerCrisis() {
    const crisisMessage = `
    <div style="display: flex; gap: 10px; align-items: start;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ef4444" width="24" height="24" style="flex-shrink: 0; margin-top: 2px;">
            <path d="M12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22ZM11 15V17H13V15H11ZM11 7V13H13V7H11Z"></path>
        </svg>
        <div>
            <strong style="color: #fca5a5; display: block; margin-bottom: 8px;">EMERGENCY RESOURCES</strong>
            If you are in immediate danger, please call emergency services (911 in US, 112 in EU).<br><br>
            <strong>US Suicide & Crisis Lifeline:</strong> 988 (Call or Text)<br>
            <strong>Crisis Text Line:</strong> Text HOME to 741741<br>
            <strong>International:</strong> <a href='https://www.findahelpline.com/' target='_blank' style='color:#64B5F6; text-decoration: underline;'>Find A Helpline</a><br><br>
            Please stay safe. You are not alone.
        </div>
    </div>
    `;

    // Send a message to the bot as well to log the event contextually
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.style = "border-left: 4px solid #ef4444; background: rgba(239, 68, 68, 0.1);";
    messageDiv.innerHTML = crisisMessage;
    chatBox.appendChild(messageDiv);
    scrollToBottom();
}

let breathingInterval;

function toggleBreathing() {
    const overlay = document.getElementById('breathing-overlay');
    const label = document.getElementById('breathing-label');
    const instruction = document.getElementById('breathing-instruction');

    if (overlay.style.display === 'flex') {
        overlay.style.display = 'none';
        // clear timeouts if any (simple approach: just stop the recursion via flag or reload)
        // For simple demo, we just hide it. The timeouts continue but don't affect invisible DOM much.
        // A better way is using requestAnimationFrame or specific timeout ID tracking.
        // For now, reload page to reset state if needed or just hide.
    } else {
        overlay.style.display = 'flex';

        let phase = 0;

        const runCycle = () => {
            if (overlay.style.display === 'none') return;

            if (phase === 0) {
                label.textContent = "Inhale";
                instruction.textContent = "Breathe in deeply...";
                phase = 1;
                setTimeout(runCycle, 4000);
            } else if (phase === 1) {
                label.textContent = "Hold";
                instruction.textContent = "Hold your breath...";
                phase = 2;
                setTimeout(runCycle, 4000);
            } else {
                label.textContent = "Exhale";
                instruction.textContent = "Breathe out slowly...";
                phase = 0;
                setTimeout(runCycle, 4000);
            }
        };
        runCycle();
    }
}
