import os
from typing import Optional

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


class LLMClient:
    def __init__(self):
        self.use_real = os.getenv("USE_REAL_LLM", "false").lower() == "true"
        self.api_key = os.getenv("MINIMAX_API_KEY", "")
        self.model = os.getenv("MODEL_NAME", "MiniMax-M2.5")
        self._client: Optional[Anthropic] = None

    @property
    def client(self) -> Optional[Anthropic]:
        if self.use_real and not self._client:
            base_url = os.getenv(
                "ANTHROPIC_BASE_URL", "https://api.minimax.io/anthropic"
            )
            self._client = Anthropic(api_key=self.api_key, base_url=base_url)
        return self._client

    def chat(self, system: str, user_message: str, max_tokens: int = 1000) -> dict:
        if not self.use_real:
            return self._mock_response(user_message)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=[
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": user_message}],
                    }
                ],
            )

            text_content = ""
            thinking_content = ""

            for block in response.content:
                if block.type == "thinking":
                    thinking_content = block.thinking
                elif block.type == "text":
                    text_content = block.text

            return {
                "response": text_content,
                "thinking": thinking_content,
                "tool_name": "MiniMax-LLM",
                "status": "success",
            }
        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "tool_name": "MiniMax-LLM",
                "status": "error",
            }

    def _mock_response(self, query: str) -> dict:
        return {
            "response": f"[MOCK MODE] Processed: {query}",
            "tool_name": "MockTool",
            "status": "success",
        }
