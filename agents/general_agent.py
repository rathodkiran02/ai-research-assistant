"""
General Agent
-------------
Handles two cases:
  1. use_tools=False → pure LLM reasoning / conversation
  2. use_tools=True  → decides which tool to call (calculator or web_search),
                       calls it, then generates a final answer using the tool result
"""

import re
from agents.llm_client import chat
from tools.calculator import calculate
from tools.web_search import web_search

TOOL_DECISION_PROMPT = """You are an AI assistant that decides which tool to use.

Available tools:
- calculator: for any math expression (e.g., "2 + 2", "sqrt(16)", "15% of 200")
- web_search: for factual lookups about people, companies, technologies, or current events

Analyze the query and respond in this exact format:
TOOL: <calculator|web_search>
INPUT: <the exact expression or search query>

Query: {query}"""

TOOL_ANSWER_PROMPT = """You are a helpful assistant. The user asked a question and a tool was used to get information.

User Question: {query}
Tool Used: {tool}
Tool Result: {result}

Provide a clear, helpful answer based on the tool result."""

GENERAL_PROMPT = """You are a helpful AI research assistant. Answer the following question clearly and concisely.

Question: {query}"""


def _parse_tool_decision(response: str) -> tuple[str, str]:
    tool_match = re.search(r"TOOL:\s*(calculator|web_search)", response, re.IGNORECASE)
    input_match = re.search(r"INPUT:\s*(.+)", response)
    tool = tool_match.group(1).lower() if tool_match else "web_search"
    tool_input = input_match.group(1).strip() if input_match else ""
    return tool, tool_input


def general_agent(query: str, use_tools: bool = False) -> dict:
    tool_info = None

    if use_tools:
        decision = chat([
            {"role": "user", "content": TOOL_DECISION_PROMPT.format(query=query)}
        ])
        tool_name, tool_input = _parse_tool_decision(decision)

        if tool_name == "calculator":
            tool_result = calculate(tool_input)
            result_str = f"Result: {tool_result['result']}" if tool_result["error"] is None else f"Error: {tool_result['error']}"
        else:
            tool_result = web_search(tool_input)
            result_str = tool_result["result"]

        tool_info = {"tool": tool_name, "input": tool_input, "output": result_str}

        answer = chat([
            {"role": "user", "content": TOOL_ANSWER_PROMPT.format(
                query=query, tool=tool_name, result=result_str
            )}
        ])
    else:
        answer = chat([
            {"role": "user", "content": GENERAL_PROMPT.format(query=query)}
        ])

    return {
        "agent": "GeneralAgent",
        "answer": answer,
        "tool_used": tool_info,
        "retrieved_chunks": [],
    }
