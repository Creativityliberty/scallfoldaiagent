const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const messages = document.getElementById('messages');
const streamMode = document.getElementById('stream-mode');
const showTrace = document.getElementById('show-trace');
const debugPanel = document.getElementById('debug-panel');
const traceOutput = document.getElementById('trace-output');

// GitMCP elements
const gitmcpUrl = document.getElementById('gitmcp-url');
const gitmcpBtn = document.getElementById('gitmcp-btn');
const gitmcpStatus = document.getElementById('gitmcp-status');

// Store repo context
let repoContext = null;

// Gestion de la trace
showTrace.addEventListener('change', () => {
  debugPanel.classList.toggle('hidden', !showTrace.checked);
});

// Ajouter un message à l'interface
function addMessage(role, content, meta = null) {
  const div = document.createElement('div');
  div.className = `message ${role}`;
  
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = content;
  
  div.appendChild(bubble);
  
  if (meta) {
    const metaDiv = document.createElement('div');
    metaDiv.className = 'meta';
    metaDiv.textContent = `⏱️ ${meta.duration || 'N/A'}ms | 🎯 ${(meta.confidence * 100).toFixed(0)}%`;
    div.appendChild(metaDiv);
  }
  
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  
  return bubble;
}

// Support for system messages (GitMCP context, etc)
function addSystemMessage(content) {
  return addMessage('system', content);
}

// Afficher la trace
function displayTrace(trace) {
  traceOutput.textContent = JSON.stringify(trace, null, 2);
}

// Mode REST (non-streaming)
async function sendMessage(text) {
  const userMsg = addMessage('user', text);
  
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: text })
    });
    
    const data = await res.json();
    
    addMessage('assistant', data.answer, {
      duration: data.meta?.trace?.reduce((sum, t) => sum + t.duration_ms, 0) || 0,
      confidence: data.meta?.confidence || 0
    });
    
    if (showTrace.checked) {
      displayTrace(data.meta);
    }
    
  } catch (err) {
    addMessage('assistant', `❌ Erreur: ${err.message}`);
  }
}

// Mode SSE (streaming)
async function streamMessage(text) {
  addMessage('user', text);
  const bubble = addMessage('assistant', '');
  
  const params = new URLSearchParams({ prompt: text });
  const eventSource = new EventSource(`/api/stream?${params}`);
  
  eventSource.onmessage = (e) => {
    bubble.textContent += e.data;
    messages.scrollTop = messages.scrollHeight;
  };
  
  eventSource.addEventListener('done', () => {
    eventSource.close();
  });
  
  eventSource.addEventListener('error', () => {
    eventSource.close();
    bubble.textContent += '\n[Erreur de streaming]';
  });
}

// GitMCP: Fetch repo context
async function fetchGitMCPContext(url) {
  gitmcpStatus.textContent = '⏳ Chargement...';
  gitmcpStatus.className = 'gitmcp-status loading';
  
  try {
    const res = await fetch('/api/gitmcp/fetch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    
    const data = await res.json();
    
    if (data.success) {
      repoContext = data;
      gitmcpStatus.textContent = `✅ Repo chargé: ${data.url}`;
      gitmcpStatus.className = 'gitmcp-status success';
      addSystemMessage(`📦 Contexte repo chargé:\n${data.url}`);
    } else {
      gitmcpStatus.textContent = `❌ Erreur: ${data.error}`;
      gitmcpStatus.className = 'gitmcp-status error';
    }
  } catch (err) {
    gitmcpStatus.textContent = `❌ Erreur: ${err.message}`;
    gitmcpStatus.className = 'gitmcp-status error';
  }
}

// GitMCP button handler
gitmcpBtn.addEventListener('click', async () => {
  const url = gitmcpUrl.value.trim();
  if (!url) {
    gitmcpStatus.textContent = '⚠️ Colle une URL';
    gitmcpStatus.className = 'gitmcp-status warning';
    return;
  }
  await fetchGitMCPContext(url);
});

// GitMCP: Allow Enter key in URL field
gitmcpUrl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    gitmcpBtn.click();
  }
});

// Gestion du formulaire
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  
  input.value = '';
  
  // Inject repo context if available
  let finalText = text;
  if (repoContext && repoContext.success) {
    finalText = `[Contexte Repo: ${repoContext.url}]\n${text}`;
  }
  
  if (streamMode.checked) {
    await streamMessage(finalText);
  } else {
    await sendMessage(finalText);
  }
});

// Shift+Enter = stream
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && e.shiftKey) {
    e.preventDefault();
    streamMode.checked = true;
    form.dispatchEvent(new Event('submit'));
  }
});
