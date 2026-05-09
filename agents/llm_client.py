import time
from openai import OpenAI, RateLimitError
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, LLM_MODEL


def get_llm_client() -> OpenAI:
    return OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL)


def chat(messages: list[dict], client: OpenAI = None, retries: int = 3) -> str:
    if client is None:
        client = get_llm_client()
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages,
            )
            return response.choices[0].message.content.strip()
        except RateLimitError:
            wait = 30 * (attempt + 1)
            print(f"[LLM] Rate limited. Waiting {wait}s before retry {attempt + 1}/{retries}...")
            time.sleep(wait)
    raise RuntimeError("LLM rate limit exceeded after retries. Please wait a minute and try again.")
