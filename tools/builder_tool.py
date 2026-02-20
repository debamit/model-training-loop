from typing import Optional

import json

import requests

from tools.llm_client import LLMClient


GOAL_TYPES = ["payment", "travel", "research", "general"]

CLASSIFIER_PROMPT = """Classify the user intent based on their query.
Respond ONLY with valid JSON in this exact format:
{{"goal_type": "payment" | "travel" | "research" | "general", "confidence": 0.0-1.0, "reasoning": "brief explanation"}}

Rules:
- payment: bills, transfers, financial transactions
- travel: trips, flights, hotels, vacation planning
- research: finding information, searches, learning
- general: anything else

Query: {user_query}"""


class BuilderTool:
    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = """You are a helpful AI assistant that provides fast, accurate responses.
You should be concise and actionable in your answers."""

    def classify_intent(self, user_query: str) -> dict:
        prompt = CLASSIFIER_PROMPT.format(user_query=user_query)
        result = self.llm.chat(
            system="You are an intent classification assistant. Respond only with valid JSON.",
            user_message=prompt,
        )
        response_text = result.get("response", "{}")
        try:
            parsed = json.loads(response_text)
            if parsed.get("goal_type") in GOAL_TYPES:
                return parsed
        except (json.JSONDecodeError, KeyError):
            pass
        return {
            "goal_type": "general",
            "confidence": 0.5,
            "reasoning": "fallback to general",
        }

    def fetch_country_data(self, country_name: Optional[str] = None) -> dict:
        try:
            url = "https://restcountries.com/v3.1/all"
            params = {
                "fields": "name,capital,region,subregion,currencies,languages,population"
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                countries = response.json()
                if country_name:
                    country_name_lower = country_name.lower()
                    for c in countries:
                        if (
                            country_name_lower
                            in c.get("name", {}).get("common", "").lower()
                        ):
                            return {"found": True, "data": c}
                    return {"found": False, "data": None}
                return {"found": True, "data": countries[:10]}
            return {"found": False, "error": f"API returned {response.status_code}"}
        except Exception as e:
            return {"found": False, "error": str(e)}

    def execute(self, user_query: str, context: Optional[dict] = None) -> dict:
        ctx = context or {}
        mode = ctx.get("mode")

        if mode == "classify_only":
            return self.classify_intent(user_query)

        goal_type = ctx.get("goal_type", "general")

        if goal_type == "travel":
            country_data = self.fetch_country_data()
            ctx["country_context"] = country_data

        result = self.llm.chat(system=self.system_prompt, user_message=user_query)

        country_context = ctx.get("country_context")
        if goal_type == "travel" and country_context:
            result["country_data"] = country_context

        return result
