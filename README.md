# 🔬 AI Research Assistant — Multi-Agent RAG System

A production-quality multi-agent AI system that answers user queries using **Retrieval-Augmented Generation (RAG)**, **tool usage**, and **intelligent agent orchestration**.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      User Query                         │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               Coordinator Agent                         │
│  • Classifies query intent via LLM                      │
│  • Routes to: RAG | TOOL | GENERAL                      │
└──────────┬──────────────┬──────────────────┬────────────┘
           │              │                  │
           ▼              ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│  Retriever   │  │   General    │  │   General Agent  │
│    Agent     │  │    Agent     │  │  (no tools)      │
│  (RAG path)  │  │ (tool path)  │  │  (reasoning)     │
└──────┬───────┘  └──────┬───────┘  └──────────────────┘
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────────────────┐
│   DuckDB     │  │  Tools                   │
│  Vector      │  │  ├── Calculator           │
│  Store       │  │  └── Web Search (mocked) │
└──────┬───────┘  └──────────────────────────┘
       │
       ▼
┌──────────────┐
│  Documents   │
│  (MD/TXT/PDF)│
└──────────────┘
```

---

## 📁 Project Structure

```
delhphi/
├── agents/
│   ├── coordinator.py       # Routes queries to correct agent
│   ├── retriever_agent.py   # Handles RAG queries
│   ├── general_agent.py     # Handles reasoning + tool calls
│   └── llm_client.py        # OpenRouter LLM wrapper
├── rag/
│   ├── loader.py            # Loads & chunks documents
│   ├── embedder.py          # Sentence-transformer embeddings
│   └── store.py             # DuckDB vector store + retrieval
├── tools/
│   ├── calculator.py        # Safe AST-based math evaluator
│   └── web_search.py        # Mocked web search tool
├── documents/
│   ├── ai_research.md       # AI/ML knowledge base doc
│   ├── climate_change.md    # Climate science doc
│   └── space_exploration.md # Space missions doc
├── data/                    # DuckDB database (auto-created)
├── app.py                   # Streamlit web UI
├── main.py                  # CLI entry point
├── config.py                # All configuration constants
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/rathodkiran02/ai-research-assistant.git
cd ai-research-assistant
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
- Sign up at [openrouter.ai](https://openrouter.ai)
- Go to **Keys** → Create a new key (free tier available)
- Copy `.env.example` to `.env` and paste your key:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENROUTER_API_KEY=sk-or-your-actual-key-here
```

### 5. Run the app

**Streamlit UI (recommended):**
```bash
streamlit run app.py
```

**CLI mode:**
```bash
python main.py
```

---

## 🚀 How It Works

### Query Routing (Coordinator Agent)
The Coordinator uses the LLM to classify every query into one of three routes **before** doing any work:

| Route | When Used | Agent Invoked |
|-------|-----------|---------------|
| `rag` | Questions about AI, climate, space, or document topics | RetrieverAgent |
| `tool` | Math calculations or factual web lookups | GeneralAgent (with tools) |
| `general` | Conversation, coding help, opinions | GeneralAgent (no tools) |

This avoids the common pitfall of **always calling RAG** — only queries that genuinely need document context trigger retrieval.

### RAG Pipeline
1. **Load** — Documents (`.md`, `.txt`, `.pdf`) are loaded from `documents/`
2. **Chunk** — Text is split into 500-character overlapping chunks (50-char overlap)
3. **Embed** — Each chunk is embedded using `all-MiniLM-L6-v2` (local, free)
4. **Store** — Embeddings stored in DuckDB as JSON-serialized vectors
5. **Retrieve** — At query time, cosine similarity ranks all chunks, top-3 returned
6. **Generate** — LLM answers using retrieved chunks as context

Retrieved chunks are **always shown** in the UI for full transparency.

### Tools
- **Calculator**: Uses Python's `ast` module to safely evaluate math expressions without `eval()`. Supports `+`, `-`, `*`, `/`, `**`, `%`.
- **Web Search**: Mocked search with keyword matching. Replace `_MOCK_DB` in `tools/web_search.py` with a real API (SerpAPI, Brave) for production.

---

## 🎯 Design Decisions

### Why DuckDB instead of a vector database?
DuckDB is a lightweight, file-based analytical database that requires zero infrastructure setup. For a demo/prototype, it's perfect — no Docker, no cloud services. The cosine similarity is computed in Python with NumPy. For production scale, swap to pgvector or Pinecone.

### Why sentence-transformers locally?
`all-MiniLM-L6-v2` is free, fast, and runs entirely locally — no API calls needed for embeddings. This keeps costs at zero and latency low.

### Why OpenRouter?
OpenRouter provides a unified API for many LLMs including free-tier models like Mistral-7B. It's OpenAI-compatible, so the `openai` Python SDK works without modification.

### Why AST-based calculator instead of `eval()`?
`eval()` is a security risk — it can execute arbitrary Python code. The AST-based approach only allows safe mathematical operations.

### Real multi-agent separation
Each agent has a **single responsibility**:
- Coordinator only classifies and routes
- RetrieverAgent only does RAG
- GeneralAgent only does reasoning/tools

They don't share state and communicate only through structured return dictionaries.

---

## ⚖️ Tradeoffs

| Decision | Benefit | Tradeoff |
|----------|---------|----------|
| DuckDB for vectors | Zero setup, portable | Not scalable to millions of docs |
| Local embeddings | Free, no latency | Slower first load (model download) |
| Mocked web search | No API key needed | Not real-time data |
| LLM-based routing | Flexible, understands nuance | Adds one LLM call per query |
| Chunk size 500 chars | Good context density | May split mid-sentence |

---

## 📊 Sample Evaluation Dataset

| Query | Expected Route | Expected Agent |
|-------|---------------|----------------|
| "What is RAG?" | rag | RetrieverAgent |
| "Explain deep learning" | rag | RetrieverAgent |
| "What causes climate change?" | rag | RetrieverAgent |
| "When did Apollo 11 land on the moon?" | rag | RetrieverAgent |
| "Calculate 15% of 2500" | tool | GeneralAgent |
| "What is 2^10 + 50?" | tool | GeneralAgent |
| "Who is Elon Musk?" | tool | GeneralAgent |
| "What is quantum computing?" | tool | GeneralAgent |
| "Write a haiku about space" | general | GeneralAgent |
| "What is the capital of France?" | general | GeneralAgent |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Mistral-7B via OpenRouter |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | DuckDB |
| Agent Framework | Custom (no heavy framework dependency) |
| UI | Streamlit |
| Math Tool | Python AST |
| Search Tool | Mocked (extensible) |

---

## 🔮 Future Improvements

- [ ] Replace mocked search with real API (Brave Search / SerpAPI)
- [ ] Add PDF upload in Streamlit UI
- [ ] Streaming LLM responses
- [ ] Conversation memory across turns
- [ ] Swap DuckDB for pgvector for production scale
- [ ] Add logging/tracing with LangSmith or custom logger
- [ ] Re-ranking retrieved chunks with a cross-encoder

---

## 👤 Author

**Kiran Rathod**
GitHub: [@rathodkiran02](https://github.com/rathodkiran02)
