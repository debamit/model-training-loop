from typing import Optional

from tools.llm_client import LLMClient


class BuilderTool:
    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = """You are a helpful AI assistant that provides fast, accurate responses.
You should be concise and actionable in your answers."""

    def execute(self, user_query: str, context: Optional[dict] = None) -> dict:
        result = self.llm.chat(system=self.system_prompt, user_message=user_query)
        return result
