"""
Coordinator Agent
-----------------
Classifies the user query into one of three routes:
  - "rag"        → needs document knowledge base
  - "tool"       → needs calculator or web search
  - "general"    → general reasoning / conversation
Then delegates to the appropriate agent.
"""

from agents.llm_client import chat
from agents.retriever_agent import retriever_agent
from agents.general_agent import general_agent

CLASSIFY_PROMPT = """You are a query router. Classify the user query into exactly one category:

- "rag"     : The query asks about AI, climate change, space exploration, or any topic likely covered in a document knowledge base.
- "tool"    : The query requires a calculation (math expression) OR a factual web lookup about a specific person, company, or technology NOT in the knowledge base.
- "general" : General conversation, opinions, coding help, or anything else.

Respond with ONLY one word: rag, tool, or general.

Query: {query}"""


def classify_query(query: str) -> str:
    response = chat([
        {"role": "user", "content": CLASSIFY_PROMPT.format(query=query)}
    ])
    label = response.strip().lower()
    if label not in ("rag", "tool", "general"):
        return "general"
    return label


def coordinator_agent(query: str) -> dict:
    """
    Main entry point. Routes query and returns structured result.
    """
    route = classify_query(query)

    if route == "rag":
        result = retriever_agent(query)
    elif route == "tool":
        result = general_agent(query, use_tools=True)
    else:
        result = general_agent(query, use_tools=False)

    result["route"] = route
    return result
