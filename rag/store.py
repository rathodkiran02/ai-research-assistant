import os
import json
import duckdb
import numpy as np
from config import DUCKDB_PATH, TOP_K_RESULTS
from rag.embedder import embed_texts, embed_query


def _get_conn():
    os.makedirs(os.path.dirname(DUCKDB_PATH), exist_ok=True)
    conn = duckdb.connect(DUCKDB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY,
            source TEXT,
            text TEXT,
            embedding TEXT
        )
    """)
    return conn


def is_populated() -> bool:
    conn = _get_conn()
    count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    conn.close()
    return count > 0


def store_chunks(chunks: list[dict]):
    conn = _get_conn()
    conn.execute("DELETE FROM chunks")
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        conn.execute(
            "INSERT INTO chunks VALUES (?, ?, ?, ?)",
            [i, chunk["source"], chunk["text"], json.dumps(emb)]
        )
    conn.close()
    print(f"[Store] Stored {len(chunks)} chunks in DuckDB.")


def retrieve(query: str, top_k: int = TOP_K_RESULTS) -> list[dict]:
    conn = _get_conn()
    rows = conn.execute("SELECT id, source, text, embedding FROM chunks").fetchall()
    conn.close()

    if not rows:
        return []

    query_emb = np.array(embed_query(query))
    scored = []
    for row in rows:
        emb = np.array(json.loads(row[3]))
        score = float(np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb) + 1e-9))
        scored.append({"source": row[1], "text": row[2], "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
