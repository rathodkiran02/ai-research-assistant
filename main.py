"""
CLI entry point for the AI Research Assistant.
Run: python main.py
"""

from rag.loader import load_documents, chunk_documents
from rag.store import store_chunks, is_populated
from agents.coordinator import coordinator_agent


def setup_knowledge_base():
    if not is_populated():
        print("[Setup] Loading and indexing documents...")
        docs = load_documents()
        chunks = chunk_documents(docs)
        store_chunks(chunks)
        print(f"[Setup] Done. {len(chunks)} chunks indexed.\n")
    else:
        print("[Setup] Knowledge base already populated.\n")


def print_result(result: dict):
    print("\n" + "=" * 60)
    print(f"Route  : {result.get('route', '').upper()}")
    print(f"Agent  : {result.get('agent', '')}")
    print("-" * 60)
    print(f"Answer :\n{result['answer']}")

    chunks = result.get("retrieved_chunks", [])
    if chunks:
        print("\n--- Retrieved Chunks ---")
        for i, c in enumerate(chunks, 1):
            print(f"\n[{i}] Source: {c['source']} | Score: {c['score']:.3f}")
            print(c["text"][:300] + "..." if len(c["text"]) > 300 else c["text"])

    tool = result.get("tool_used")
    if tool:
        print(f"\n--- Tool Used ---")
        print(f"Tool  : {tool['tool']}")
        print(f"Input : {tool['input']}")
        print(f"Output: {tool['output']}")

    print("=" * 60 + "\n")


def main():
    print("🔬 AI Research Assistant (CLI)")
    print("Type 'quit' to exit.\n")
    setup_knowledge_base()

    while True:
        query = input("You: ").strip()
        if not query:
            continue
        if query.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        result = coordinator_agent(query)
        print_result(result)


if __name__ == "__main__":
    main()
