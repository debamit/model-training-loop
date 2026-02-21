import json
import os
from pathlib import Path
from typing import Any, Optional

CONFIG_FILE = Path(__file__).parent.parent / "config.json"

_config: Optional[dict[str, Any]] = None


def load_config() -> dict[str, Any]:
    global _config
    if _config is not None:
        return _config

    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            _config = json.load(f)
    else:
        _config = {"providers": {}, "agents": {"defaults": {}}}

    return _config


def get_provider_config(name: str) -> Optional[dict[str, Any]]:
    config = load_config()
    providers = config.get("providers", {})

    if name in providers:
        return providers[name]

    env_key = f"{name.upper()}_API_KEY"
    api_key = os.getenv(env_key)

    if api_key:
        provider_config = {"apiKey": api_key}

        if name == "minimax":
            provider_config["apiBase"] = "https://api.minimax.io/anthropic"

        return provider_config

    return None


def get_model_config() -> dict[str, Any]:
    config = load_config()
    defaults = config.get("agents", {}).get("defaults", {})

    if defaults.get("model") and defaults.get("provider"):
        return defaults

    if os.getenv("MINIMAX_API_KEY"):
        return {"model": "MiniMax-M2.5", "provider": "minimax"}
    elif os.getenv("ANTHROPIC_API_KEY"):
        return {"model": "claude-sonnet-4-5-20250929", "provider": "anthropic"}
    elif os.getenv("OPENAI_API_KEY"):
        return {"model": "gpt-4o", "provider": "openai"}

    return {"model": "MiniMax-M2.5", "provider": "minimax"}


def create_chat_model(
    model: Optional[str] = None,
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
):
    from langchain.chat_models import init_chat_model

    model_config = get_model_config()

    provider = provider or model_config.get("provider", "minimax")
    model = model or model_config.get("model", "MiniMax-M2.5")

    provider_config = get_provider_config(provider)

    if provider_config:
        api_key = api_key or provider_config.get("apiKey")
        api_base = api_base or provider_config.get("apiBase")

    if not api_key:
        env_key = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(env_key)

    os.environ.pop("ANTHROPIC_BASE_URL", None)
    os.environ.pop("ANTHROPIC_API_KEY", None)
    os.environ.pop("OPENAI_API_KEY", None)

    if provider == "minimax":
        os.environ["ANTHROPIC_BASE_URL"] = (
            api_base or "https://api.minimax.io/anthropic"
        )
        os.environ["ANTHROPIC_API_KEY"] = api_key or ""
        model_provider = "anthropic"
        print(f"Using MiniMax API (Anthropic-compatible)")
    elif provider == "anthropic":
        if not api_key:
            raise ValueError(
                "anthropic provider requires apiKey in config or ANTHROPIC_API_KEY env var"
            )
        os.environ["ANTHROPIC_API_KEY"] = api_key
        model_provider = "anthropic"
        print(f"Using Anthropic API")
    elif provider == "openai":
        if not api_key:
            raise ValueError(
                "openai provider requires apiKey in config or OPENAI_API_KEY env var"
            )
        os.environ["OPENAI_API_KEY"] = api_key
        model_provider = "openai"
        print(f"Using OpenAI API")
    elif provider == "custom":
        if api_base:
            os.environ["OPENAI_API_KEY"] = api_key or "dummy"
            os.environ["OPENAI_BASE_URL"] = api_base
            model_provider = "openai"
            print(f"Using Custom provider at {api_base}")
        else:
            raise ValueError("custom provider requires apiBase in config")
    else:
        raise ValueError(f"Unknown provider: {provider}")

    return init_chat_model(model=model, model_provider=model_provider)
