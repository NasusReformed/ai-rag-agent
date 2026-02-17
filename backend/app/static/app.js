const API_BASE = 'http://localhost:8000/api';
let currentSessionId = null;

// Check API status
async function checkApiStatus() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
            setApiStatus('ok');
        } else {
            setApiStatus('error');
        }
    } catch (error) {
        setApiStatus('error');
    }
}

function setApiStatus(status) {
    const statusEl = document.getElementById('apiStatus');
    statusEl.textContent = status === 'ok' ? '✅ Connected' : '❌ Disconnected';
    statusEl.className = `status-${status === 'ok' ? 'ok' : 'error'}`;
}

// Tab switching
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.add('active');
    });
});

// Chat functionality
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    input.value = '';

    try {
        const response = await fetch(`${API_BASE}/agent/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: currentSessionId,
                user_id: 'demo_user',
                message: message
            })
        });

        if (!response.ok) throw new Error('Failed to get response');
        const data = await response.json();
        currentSessionId = data.session_id;
        addMessage(data.answer, 'assistant');

        if (data.sources && data.sources.length > 0) {
            addMessage(`📚 Sources: ${data.sources.length} documents found`, 'system');
        }
    } catch (error) {
        addMessage(`Error: ${error.message}`, 'system');
    }
}

function addMessage(text, role) {
    const messagesDiv = document.getElementById('messages');
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    messageEl.innerHTML = `<p>${escapeHtml(text)}</p>`;
    messagesDiv.appendChild(messageEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Load demo data
async function loadDemoData() {
    const btn = event.target;
    btn.disabled = true;
    btn.textContent = 'Loading...';
    
    try {
        const demoRes = await fetch(`${API_BASE}/demo/seed-data`);
        const demoData = await demoRes.json();
        
        // Index all demo documents
        const indexRes = await fetch(`${API_BASE}/embeddings/index`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ documents: demoData.documents })
        });
        
        if (!indexRes.ok) throw new Error('Failed to index demo data');
        const result = await indexRes.json();
        
        const statusEl = document.getElementById('indexStatus');
        statusEl.textContent = `✅ Loaded ${result.indexed} demo documents! Try searching or chatting.`;
        statusEl.className = 'success';
    } catch (error) {
        const statusEl = document.getElementById('indexStatus');
        statusEl.textContent = `❌ Error: ${error.message}`;
        statusEl.className = 'error';
    } finally {
        btn.disabled = false;
        btn.textContent = '📥 Load Demo Data';
    }
}

// Document indexing
async function indexDocument() {
    const content = document.getElementById('docContent').value.trim();
    const category = document.getElementById('docCategory').value.trim();
    if (!content) return;

    const statusEl = document.getElementById('indexStatus');
    statusEl.textContent = 'Indexing...';
    statusEl.className = '';

    try {
        const response = await fetch(`${API_BASE}/embeddings/index`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                documents: [{
                    content: content,
                    metadata: { category: category, source: 'dashboard' }
                }]
            })
        });

        if (!response.ok) throw new Error('Failed to index');
        const data = await response.json();
        statusEl.textContent = `✅ Indexed ${data.indexed} document(s)`;
        statusEl.className = 'success';
        document.getElementById('docContent').value = '';
    } catch (error) {
        statusEl.textContent = `❌ Error: ${error.message}`;
        statusEl.className = 'error';
    }
}

// Search functionality
async function searchDocuments() {
    const query = document.getElementById('searchQuery').value.trim();
    if (!query) return;

    const resultsEl = document.getElementById('searchResults');
    resultsEl.innerHTML = '<p>Searching...</p>';

    try {
        const response = await fetch(`${API_BASE}/embeddings/search?query=${encodeURIComponent(query)}&top_k=5`);
        const data = await response.json();
        
        if (!response.ok) throw new Error(data.detail || 'Search failed');

        if (!data || data.length === 0) {
            resultsEl.innerHTML = '<p style="color: #999;">No results found</p>';
            return;
        }

        resultsEl.innerHTML = '';
        data.forEach((item, idx) => {
            const el = document.createElement('div');
            el.className = 'result-item';
            el.innerHTML = `
                <div class="score">Score: ${(item.score * 100).toFixed(1)}%</div>
                <div class="content">${escapeHtml(item.content.substring(0, 200))}</div>
            `;
            resultsEl.appendChild(el);
        });
    } catch (error) {
        resultsEl.innerHTML = `<p style="color: #d32f2f;">Error: ${error.message}</p>`;
    }
}

// Tool execution
async function executeTool() {
    const toolName = document.getElementById('toolSelect').value;
    const title = document.getElementById('toolTitle').value.trim();
    const priority = document.getElementById('toolPriority').value;
    const resultEl = document.getElementById('toolResult');

    if (!title && toolName === 'create_ticket') {
        resultEl.textContent = 'Please enter a title';
        resultEl.className = 'error';
        return;
    }

    resultEl.textContent = 'Executing...';
    resultEl.className = '';

    try {
        const args = toolName === 'create_ticket'
            ? { title: title, priority: priority, user_id: 'demo_user', context: { source: 'dashboard' } }
            : { query: title, top_k: 3 };

        const response = await fetch(`${API_BASE}/tools/execute`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                tool_name: toolName,
                tool_args: args
            })
        });

        if (!response.ok) throw new Error('Tool execution failed');
        const data = await response.json();
        resultEl.textContent = `✅ Success: ${JSON.stringify(data.result).substring(0, 150)}...`;
        resultEl.className = 'success';
    } catch (error) {
        resultEl.textContent = `❌ Error: ${error.message}`;
        resultEl.className = 'error';
    }
}

// Allow Enter key in chat
document.getElementById('userInput')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Check API status on load and every 5s
checkApiStatus();
setInterval(checkApiStatus, 5000);
