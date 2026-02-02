/**
 * Campus AI Chat - Frontend Application
 * Handles streaming responses and user interactions
 */

// Configuration
const API_BASE_URL = window.location.origin;
const STREAM_ENDPOINT = `${API_BASE_URL}/api/chat/stream`;
const STATUS_ENDPOINT = `${API_BASE_URL}/status`;

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const serverStatus = document.getElementById('serverStatus');

// State
let isGenerating = false;
let messageCount = 0;

/**
 * Initialize the application
 */
async function init() {
    console.log('🚀 Campus AI Chat initialized');

    // Check server status
    await checkServerStatus();

    // Set up event listeners
    setupEventListeners();

    // Auto-resize textarea
    setupTextareaAutoResize();

    // Focus input
    userInput.focus();
}

/**
 * Check server status and update UI
 */
async function checkServerStatus() {
    try {
        const response = await fetch(STATUS_ENDPOINT);
        const data = await response.json();

        if (data.status === 'running' && data.model.loaded) {
            updateServerStatus('connected', `Online • ${data.current_users}/${data.max_users} users`);
        } else {
            updateServerStatus('warning', 'Server OK, Model Loading...');
        }
    } catch (error) {
        console.error('Status check failed:', error);
        updateServerStatus('error', 'Connection Error');
    }
}

/**
 * Update server status indicator
 */
function updateServerStatus(status, text) {
    serverStatus.className = `server-status ${status}`;
    serverStatus.querySelector('.status-text').textContent = text;
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    // Send button click
    sendBtn.addEventListener('click', handleSendMessage);

    // Clear button click
    clearBtn.addEventListener('click', handleClearChat);

    // Enter key to send (Shift+Enter for newline)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    // Periodic status check (every 10 seconds)
    setInterval(checkServerStatus, 10000);
}

/**
 * Auto-resize textarea as user types
 */
function setupTextareaAutoResize() {
    userInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
}

/**
 * Handle send message action
 */
async function handleSendMessage() {
    const message = userInput.value.trim();

    // Validation
    if (!message || isGenerating) return;

    // Clear input
    userInput.value = '';
    userInput.style.height = 'auto';

    // Remove welcome message if this is the first message
    if (messageCount === 0) {
        const welcomeMsg = chatMessages.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => welcomeMsg.remove(), 300);
        }
    }

    messageCount++;

    // Add user message
    addMessage('user', message);

    // Disable input while generating
    setGenerating(true);

    // Create assistant message placeholder
    const assistantMsgId = `msg-${Date.now()}`;
    addMessage('assistant', '', assistantMsgId, true);

    // Stream response
    try {
        await streamResponse(message, assistantMsgId);
    } catch (error) {
        console.error('Streaming error:', error);
        updateMessageText(assistantMsgId, '❌ Error: Could not generate response. Please try again.');
    } finally {
        setGenerating(false);
        removeTypingIndicator(assistantMsgId);
    }
}

/**
 * Add a message to the chat
 */
function addMessage(role, text, id = null, showTyping = false) {
    const messageId = id || `msg-${Date.now()}`;
    const avatar = role === 'user' ? '👤' : '🤖';

    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    messageEl.id = messageId;

    messageEl.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            ${showTyping ? `
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            ` : `
                <div class="message-text">${escapeHtml(text)}</div>
                ${role === 'assistant' ? `
                    <div class="message-actions">
                        <button class="btn-copy" onclick="copyMessage('${messageId}')">📋 Copy</button>
                    </div>
                ` : ''}
            `}
        </div>
    `;

    chatMessages.appendChild(messageEl);
    scrollToBottom();

    return messageId;
}

/**
 * Stream response from the server
 */
async function streamResponse(prompt, messageId) {
    const response = await fetch(STREAM_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt: prompt,
            max_tokens: 512,
            temperature: 0.7,
            top_p: 0.9
        })
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullText = '';
    let buffer = '';

    // Remove typing indicator
    removeTypingIndicator(messageId);

    // Create text container
    const messageEl = document.getElementById(messageId);
    const contentEl = messageEl.querySelector('.message-content');
    contentEl.innerHTML = `
        <div class="message-text"></div>
        <div class="message-actions">
            <button class="btn-copy" onclick="copyMessage('${messageId}')">📋 Copy</button>
        </div>
    `;
    const textEl = contentEl.querySelector('.message-text');

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        // Decode chunk
        buffer += decoder.decode(value, { stream: true });

        // Process complete lines
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // Keep incomplete line in buffer

        for (const line of lines) {
            if (!line.trim()) continue;

            // Parse SSE format
            if (line.startsWith('data: ')) {
                const token = line.slice(6); // Remove 'data: ' prefix

                // Unescape newlines
                const unescaped = token.replace(/\\n/g, '\n').replace(/\\r/g, '\r');

                fullText += unescaped;
                textEl.textContent = fullText;
                scrollToBottom();
            } else if (line.startsWith('event: done')) {
                console.log('✅ Stream complete');
            } else if (line.startsWith('event: error')) {
                console.error('❌ Stream error');
            }
        }
    }

    // Final update
    if (fullText) {
        textEl.textContent = fullText;
    } else {
        textEl.textContent = '(No response generated)';
    }
}

/**
 * Update message text
 */
function updateMessageText(messageId, text) {
    const messageEl = document.getElementById(messageId);
    if (!messageEl) return;

    const textEl = messageEl.querySelector('.message-text');
    if (textEl) {
        textEl.textContent = text;
    }
}

/**
 * Remove typing indicator
 */
function removeTypingIndicator(messageId) {
    const messageEl = document.getElementById(messageId);
    if (!messageEl) return;

    const typingEl = messageEl.querySelector('.typing-indicator');
    if (typingEl) {
        typingEl.remove();
    }
}

/**
 * Copy message to clipboard
 */
function copyMessage(messageId) {
    const messageEl = document.getElementById(messageId);
    const textEl = messageEl.querySelector('.message-text');

    if (!textEl) return;

    navigator.clipboard.writeText(textEl.textContent)
        .then(() => {
            const btn = messageEl.querySelector('.btn-copy');
            const originalText = btn.textContent;
            btn.textContent = '✅ Copied!';
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        })
        .catch(err => console.error('Copy failed:', err));
}

/**
 * Clear chat history
 */
function handleClearChat() {
    if (!confirm('Clear all messages?')) return;

    // Remove all messages
    const messages = chatMessages.querySelectorAll('.message');
    messages.forEach(msg => msg.remove());

    // Reset counter
    messageCount = 0;

    // Show welcome message again
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">👋</div>
            <h2>Welcome to Campus AI Chat</h2>
            <p>Your local AI assistant is ready to help. All conversations stay private on campus servers.</p>
            <div class="feature-pills">
                <span class="pill">🔒 100% Private</span>
                <span class="pill">⚡ Real-time Streaming</span>
                <span class="pill">🎯 Locally Hosted</span>
            </div>
        </div>
    `;

    userInput.focus();
}

/**
 * Set generating state
 */
function setGenerating(generating) {
    isGenerating = generating;
    sendBtn.disabled = generating;
    userInput.disabled = generating;

    if (generating) {
        sendBtn.style.opacity = '0.6';
        updateServerStatus('warning', 'Generating...');
    } else {
        sendBtn.style.opacity = '1';
        checkServerStatus();
        userInput.focus();
    }
}

/**
 * Smart scroll to bottom - only auto-scrolls if user is near bottom
 */
function scrollToBottom(force = false) {
    const threshold = 100; // pixels from bottom
    const isNearBottom = chatMessages.scrollHeight - chatMessages.scrollTop - chatMessages.clientHeight < threshold;

    // Only auto-scroll if user is near bottom or forced
    if (force || isNearBottom) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Add fadeOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; transform: scale(1); }
        to { opacity: 0; transform: scale(0.95); }
    }
`;
document.head.appendChild(style);
