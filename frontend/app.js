// === CONFIGURATION ===
const API_BASE = '';

// === DOM ELEMENTS ===
const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const messages = document.getElementById('messages');
const streamMode = document.getElementById('stream-mode');
const showTrace = document.getElementById('show-trace');
const showConfidence = document.getElementById('show-confidence');
const debugPanel = document.getElementById('debug-panel');
const traceOutput = document.getElementById('trace-output');
const closeDebug = document.getElementById('close-debug');
const loadingOverlay = document.getElementById('loading-overlay');
const statusIndicator = document.getElementById('status-indicator');
const modelInfo = document.getElementById('model-info');

// === INITIALIZATION ===
async function initApp() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    const data = await response.json();

    modelInfo.textContent = `${data.model} • ${data.mcp_tools} outils MCP`;
    statusIndicator.style.background = 'var(--success)';

    console.log('✅ App initialized', data);
  } catch (error) {
    console.error('❌ Init error:', error);
    modelInfo.textContent = 'Erreur de connexion';
    statusIndicator.style.background = 'var(--error)';
  }
}

// === EVENT LISTENERS ===
showTrace.addEventListener('change', () => {
  debugPanel.classList.toggle('hidden', !showTrace.checked);
});

closeDebug.addEventListener('click', () => {
  showTrace.checked = false;
  debugPanel.classList.add('hidden');
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  input.value = '';
  input.disabled = true;

  if (streamMode.checked) {
    await streamMessage(text);
  } else {
    await sendMessage(text);
  }

  input.disabled = false;
  input.focus();
});

// Shift+Enter = toggle stream
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && e.shiftKey) {
    e.preventDefault();
    streamMode.checked = !streamMode.checked;
  }
});

// === MESSAGE FUNCTIONS ===
function addMessage(role, content, meta = null) {
  // Remove welcome message if present
  const welcomeMsg = messages.querySelector('.welcome-message');
  if (welcomeMsg) {
    welcomeMsg.remove();
  }

  const div = document.createElement('div');
  div.className = `message ${role}`;

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = content;

  div.appendChild(bubble);

  if (meta && (meta.duration !== undefined || meta.confidence !== undefined)) {
    const metaDiv = document.createElement('div');
    metaDiv.className = 'meta';

    const parts = [];

    if (meta.duration !== undefined) {
      parts.push(`⏱️ ${meta.duration.toFixed(0)}ms`);
    }

    if (meta.confidence !== undefined && showConfidence.checked) {
      const confidencePercent = (meta.confidence * 100).toFixed(0);
      parts.push(createConfidenceBar(meta.confidence));
    }

    metaDiv.innerHTML = parts.join(' • ');
    div.appendChild(metaDiv);
  }

  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;

  return bubble;
}

function createConfidenceBar(confidence) {
  const percent = (confidence * 100).toFixed(0);
  const color = confidence > 0.7 ? 'var(--success)' : confidence > 0.4 ? 'var(--warning)' : 'var(--error)';

  return `
    <span class="confidence-bar">
      🎯 ${percent}%
      <span class="confidence-fill">
        <span class="confidence-level" style="width: ${percent}%; background: ${color}"></span>
      </span>
    </span>
  `;
}

function displayTrace(trace) {
  if (!trace) return;

  const formatted = {
    flow_id: trace.flow_id,
    trace: trace.trace,
    confidence: trace.confidence,
    status: trace.status
  };

  traceOutput.textContent = JSON.stringify(formatted, null, 2);
}

function showLoading(show) {
  loadingOverlay.classList.toggle('hidden', !show);
}

// === REST MODE ===
async function sendMessage(text) {
  addMessage('user', text);
  showLoading(true);

  try {
    const response = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: text })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    const totalDuration = data.meta?.trace?.reduce((sum, t) => sum + t.duration_ms, 0) || 0;

    addMessage('assistant', data.answer, {
      duration: totalDuration,
      confidence: data.meta?.confidence || 0
    });

    if (showTrace.checked) {
      displayTrace(data.meta);
    }

  } catch (error) {
    console.error('Chat error:', error);
    addMessage('assistant', `❌ Erreur: ${error.message}`);
  } finally {
    showLoading(false);
  }
}

// === STREAMING MODE ===
async function streamMessage(text) {
  addMessage('user', text);

  const bubble = addMessage('assistant', '');
  bubble.classList.add('streaming');

  const params = new URLSearchParams({ prompt: text });
  const eventSource = new EventSource(`${API_BASE}/api/stream?${params}`);

  let fullText = '';
  const startTime = Date.now();

  eventSource.onmessage = (e) => {
    fullText += e.data;
    bubble.textContent = fullText;
    messages.scrollTop = messages.scrollHeight;
  };

  eventSource.addEventListener('done', () => {
    eventSource.close();
    bubble.classList.remove('streaming');

    const duration = Date.now() - startTime;

    // Add meta info
    const metaDiv = document.createElement('div');
    metaDiv.className = 'meta';
    metaDiv.innerHTML = `⏱️ ${duration}ms • 📡 Streaming`;
    bubble.parentElement.appendChild(metaDiv);
  });

  eventSource.addEventListener('error', (e) => {
    console.error('SSE error:', e);
    eventSource.close();
    bubble.textContent += '\n\n❌ [Erreur de streaming]';
    bubble.classList.remove('streaming');
  });
}

// === UTILITY FUNCTIONS ===
function clearChat() {
  messages.innerHTML = '';
  traceOutput.textContent = '';
}

function exportChat() {
  const chatMessages = Array.from(messages.querySelectorAll('.message')).map(msg => ({
    role: msg.classList.contains('user') ? 'user' : 'assistant',
    content: msg.querySelector('.bubble').textContent
  }));

  const blob = new Blob([JSON.stringify(chatMessages, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `chat-export-${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

// === KEYBOARD SHORTCUTS ===
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + K = Clear chat
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    if (confirm('Effacer la conversation ?')) {
      clearChat();
    }
  }

  // Ctrl/Cmd + D = Toggle debug
  if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
    e.preventDefault();
    showTrace.checked = !showTrace.checked;
    showTrace.dispatchEvent(new Event('change'));
  }

  // Ctrl/Cmd + S = Toggle streaming
  if ((e.ctrlKey || e.metaKey) && e.key === 's') {
    e.preventDefault();
    streamMode.checked = !streamMode.checked;
  }
});

// === START APP ===
initApp();

// Make functions available globally for debugging
window.clearChat = clearChat;
window.exportChat = exportChat;

console.log('%c🤖 Agent IA Frontend Ready', 'color: #5b9cff; font-size: 16px; font-weight: bold');
console.log('Shortcuts:');
console.log('  Ctrl+K: Clear chat');
console.log('  Ctrl+D: Toggle debug');
console.log('  Ctrl+S: Toggle streaming');
console.log('  Shift+Enter: Toggle streaming (in input)');
