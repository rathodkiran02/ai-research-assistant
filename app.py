import streamlit as st
from rag.loader import load_documents, chunk_documents
from rag.store import store_chunks, is_populated
from agents.coordinator import coordinator_agent

st.set_page_config(page_title="AI Research Assistant", page_icon="🔬", layout="wide")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🔬 AI Research Assistant")
    st.markdown("**Multi-Agent RAG System**")
    st.divider()

    st.markdown("### 📚 Knowledge Base")
    if st.button("🔄 Load & Index Documents", use_container_width=True):
        with st.spinner("Loading and indexing documents..."):
            docs = load_documents()
            chunks = chunk_documents(docs)
            store_chunks(chunks)
        st.success(f"✅ Indexed {len(chunks)} chunks from {len(docs)} documents")

    if is_populated():
        st.info("✅ Knowledge base is ready")
    else:
        st.warning("⚠️ Click above to load documents first")

    st.divider()
    st.markdown("### 🤖 Agents")
    st.markdown("- **Coordinator** — routes queries")
    st.markdown("- **RetrieverAgent** — RAG + DuckDB")
    st.markdown("- **GeneralAgent** — reasoning + tools")
    st.divider()
    st.markdown("### 🛠️ Tools")
    st.markdown("- **Calculator** — math expressions")
    st.markdown("- **Web Search** — factual lookups")
    st.divider()
    st.markdown("### 💡 Try These Queries")
    st.code("What is RAG?")
    st.code("What causes climate change?")
    st.code("Calculate 15% of 2500")
    st.code("Who is Elon Musk?")
    st.code("What is the ISS?")

# ── Main Area ─────────────────────────────────────────────────────────────────
st.title("🔬 AI Research Assistant")
st.caption("Multi-Agent system with RAG, Tools, and Intelligent Routing")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
query = st.chat_input("Ask me anything...")

if query:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Run agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = coordinator_agent(query)

        # ── Route Badge ──
        route_colors = {"rag": "🟢", "tool": "🔵", "general": "🟡"}
        route = result.get("route", "general")
        agent = result.get("agent", "GeneralAgent")
        st.markdown(
            f"{route_colors.get(route, '⚪')} **Route:** `{route.upper()}` &nbsp;|&nbsp; "
            f"**Agent:** `{agent}`"
        )

        # ── Answer ──
        st.markdown("### 💬 Answer")
        st.markdown(result["answer"])

        # ── Retrieved Chunks (RAG Transparency) ──
        chunks = result.get("retrieved_chunks", [])
        if chunks:
            st.markdown("### 📄 Retrieved Context (RAG Transparency)")
            for i, chunk in enumerate(chunks, 1):
                with st.expander(f"Chunk {i} — {chunk['source']} (score: {chunk['score']:.3f})"):
                    st.markdown(chunk["text"])

        # ── Tool Usage ──
        tool_info = result.get("tool_used")
        if tool_info:
            st.markdown("### 🛠️ Tool Used")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Tool:** `{tool_info['tool']}`")
                st.markdown(f"**Input:** `{tool_info['input']}`")
            with col2:
                st.markdown(f"**Output:** {tool_info['output']}")

        # Save to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"]
        })
