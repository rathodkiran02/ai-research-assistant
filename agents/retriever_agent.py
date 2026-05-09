"""
Retriever Agent
---------------
Handles queries that require document knowledge.
1. Retrieves top-K relevant chunks from DuckDB
2. Builds a context-aware prompt
3. Calls LLM with retrieved context
4. Returns answer + retrieved chunks (for transparency)
"""

from rag.store import retrieve
from agents.llm_client import chat

RAG_PROMPT = """You are a knowledgeable research assistant. Answer the user's question using ONLY the context provided below.
If the context does not contain enough information, say so clearly.

Context:
{context}

Question: {query}

Answer:"""


def retriever_agent(query: str) -> dict:
    chunks = retrieve(query)

    if not chunks:
        return {
            "agent": "RetrieverAgent",
            "answer": "No relevant documents found in the knowledge base.",
            "retrieved_chunks": [],
        }

    context = "\n\n---\n\n".join(
        f"[Source: {c['source']} | Score: {c['score']:.3f}]\n{c['text']}"
        for c in chunks
    )

    answer = chat([
        {"role": "user", "content": RAG_PROMPT.format(context=context, query=query)}
    ])

    return {
        "agent": "RetrieverAgent",
        "answer": answer,
        "retrieved_chunks": chunks,
    }
