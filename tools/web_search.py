"""
Mocked web search tool.
In production, replace _MOCK_DB with a real search API (e.g., SerpAPI, Brave Search).
"""

_MOCK_DB = {
    "python": "Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum in 1991.",
    "openai": "OpenAI is an AI research company known for creating GPT-4, DALL-E, and ChatGPT. Founded in 2015.",
    "nasa": "NASA (National Aeronautics and Space Administration) is the US government agency responsible for the civilian space program and aerospace research.",
    "elon musk": "Elon Musk is a tech entrepreneur and CEO of Tesla and SpaceX. He also owns X (formerly Twitter).",
    "bitcoin": "Bitcoin is a decentralized digital currency created in 2009 by an anonymous person/group known as Satoshi Nakamoto.",
    "quantum computing": "Quantum computing uses quantum mechanical phenomena like superposition and entanglement to perform computations far faster than classical computers for certain problems.",
    "default": "No specific result found. This is a mocked search tool. In production, connect to a real search API."
}


def web_search(query: str) -> dict:
    """
    Mock web search. Returns a result based on keyword matching.
    Returns: {"query": ..., "result": ..., "source": "mock"}
    """
    query_lower = query.lower()
    for key, value in _MOCK_DB.items():
        if key in query_lower:
            return {"query": query, "result": value, "source": "mock_db"}
    return {"query": query, "result": _MOCK_DB["default"], "source": "mock_db"}
