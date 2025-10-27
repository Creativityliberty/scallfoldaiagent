# 🏗️ Architecture - GitMCP Integration

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Browser)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  GitMCP Section                                          │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │ Input: github.com/user/repo                    │    │   │
│  │  │ Button: 📦 Charger Repo                        │    │   │
│  │  │ Status: ⏳ Chargement... / ✅ Chargé / ❌ Erreur│   │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Chat Interface                                          │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │ Messages (user, assistant, system)             │    │   │
│  │  │ Input: Pose une question...                    │    │   │
│  │  │ Button: Envoyer                                │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
                    (HTTP REST + SSE)
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  POST /api/gitmcp/fetch                                 │   │
│  │  ├─ Receive: { "url": "github.com/user/repo" }         │   │
│  │  └─ Call: GitMCPClient.fetch_context()                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  GitMCPClient (backend/integrations/gitmcp.py)          │   │
│  │  ├─ normalize_url()                                      │   │
│  │  │  └─ github.com/user/repo → gitmcp.io/user/repo      │   │
│  │  ├─ fetch_context()                                      │   │
│  │  │  ├─ _fetch_file(llms.txt)                            │   │
│  │  │  ├─ _fetch_file(llms-full.txt) [fallback]           │   │
│  │  │  └─ _fetch_file(README.md)                           │   │
│  │  └─ extract_summary()                                    │   │
│  │     └─ Format for injection                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  External: gitmcp.io (HTTP GET)                         │   │
│  │  ├─ gitmcp.io/user/repo/raw/main/llms.txt             │   │
│  │  ├─ gitmcp.io/user/repo/raw/main/llms-full.txt        │   │
│  │  └─ gitmcp.io/user/repo/raw/main/README.md            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Response: { "success": true, "llms_context": "...", ... }  │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  POST /api/chat (with context)                          │   │
│  │  ├─ Receive: { "input": "[Contexte Repo: ...]\nQ" }    │   │
│  │  └─ Call: Orchestrator.run(shared)                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  PocketFlow Orchestrator                                │   │
│  │  ├─ Perception Node                                      │   │
│  │  ├─ Interpretation Node                                  │   │
│  │  ├─ Reasoning Node (RRLA) ← Uses repo context          │   │
│  │  ├─ Synthesis Node                                       │   │
│  │  └─ Action Node                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                            ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Gemini LLM (with repo context)                         │   │
│  │  └─ Generate response with code understanding           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
                    (HTTP REST + SSE)
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Display)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ✅ Repo loaded: gitmcp.io/user/repo                            │
│  📦 Context loaded message                                       │
│  Assistant: [Contextual response with code understanding]       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Interaction

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ├─── 1. Paste GitHub URL
       │    └─ github.com/user/repo
       │
       ├─── 2. Click "📦 Charger Repo"
       │    └─ POST /api/gitmcp/fetch
       │
       ├─── 3. Receive context
       │    └─ { success: true, llms_context: "...", readme: "..." }
       │
       ├─── 4. Store in repoContext
       │    └─ let repoContext = { ... }
       │
       ├─── 5. Display status ✅
       │    └─ "Repo chargé: gitmcp.io/user/repo"
       │
       ├─── 6. User asks question
       │    └─ "Explique ce repo"
       │
       ├─── 7. Inject context
       │    └─ "[Contexte Repo: gitmcp.io/user/repo]\nExplique ce repo"
       │
       ├─── 8. POST /api/chat
       │    └─ { input: "[Contexte...]\nExplique ce repo" }
       │
       ├─── 9. Backend processes with context
       │    └─ Orchestrator.run(shared)
       │
       ├─── 10. Gemini generates response
       │    └─ Avec compréhension du code
       │
       └─── 11. Display response
            └─ Réponse contextuelle et précise
```

## Data Flow

```
GitHub Repository
       │
       ├─ llms.txt (LLM instructions)
       ├─ llms-full.txt (Full context)
       └─ README.md (Documentation)
       │
       ↓ (via gitmcp.io)
       │
GitMCP Server
       │
       ↓ (HTTP GET)
       │
Backend: GitMCPClient
       │
       ├─ normalize_url()
       ├─ fetch_context()
       └─ extract_summary()
       │
       ↓ (JSON Response)
       │
Frontend: repoContext
       │
       ├─ Store in memory
       ├─ Display status
       └─ Inject into messages
       │
       ↓ (Augmented user input)
       │
Backend: Orchestrator
       │
       ├─ Perception
       ├─ Interpretation
       ├─ Reasoning (with context)
       ├─ Synthesis
       └─ Action
       │
       ↓ (with context)
       │
Gemini LLM
       │
       ├─ Understand code
       ├─ Analyze architecture
       └─ Generate contextual response
       │
       ↓ (SSE Stream)
       │
Frontend: Display
       │
       └─ Token-by-token response
```

## State Management

```
Frontend State:

let repoContext = null;  // Initially empty

// After loading repo:
repoContext = {
  success: true,
  url: "gitmcp.io/user/repo",
  llms_context: "...",
  readme: "...",
  source: "gitmcp"
}

// When sending message:
if (repoContext && repoContext.success) {
  finalText = `[Contexte Repo: ${repoContext.url}]\n${userText}`;
}
```

## Error Handling

```
User Input (URL)
       │
       ├─ Validation
       │  └─ Empty? → Show warning ⚠️
       │
       ├─ Fetch
       │  ├─ Network error? → Show error ❌
       │  ├─ Timeout? → Show error ❌
       │  └─ 404? → Try fallback files
       │
       ├─ Response
       │  ├─ Success? → Show ✅
       │  └─ Error? → Show ❌ + message
       │
       └─ Fallback
          └─ Continue without context
```

## Performance Considerations

| Operation | Time | Notes |
|-----------|------|-------|
| URL normalization | <1ms | Regex only |
| Fetch llms.txt | 100-500ms | Network I/O |
| Fetch README | 100-500ms | Network I/O |
| Total fetch | 200-1000ms | Parallel requests |
| Injection | <1ms | String concat |
| LLM processing | 1-5s | Depends on Gemini |

## Security & Limitations

```
✅ Supported:
  - Public GitHub repos
  - github.com URLs
  - github.io URLs
  - .git suffix handling

❌ Not supported:
  - Private repos (no auth)
  - Large repos (>10MB files)
  - Binary files
  - Submodules

⚠️ Considerations:
  - Timeout: 10 seconds
  - Rate limiting: GitHub API limits
  - Cache: None (fresh fetch each time)
  - Storage: In-memory only
```

## Integration Points

```
┌─────────────────────────────────────────────────────────────┐
│                    Future Enhancements                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Vector Store Integration                            │   │
│  │ └─ Index repo context for semantic search          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ MCP Tools Integration                               │   │
│  │ └─ Call MCP tools with repo context                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ GitHub Token Support                                │   │
│  │ └─ Access private repos                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Local Cache                                         │   │
│  │ └─ Cache repos locally for faster access           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```
