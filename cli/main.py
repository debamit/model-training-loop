import argparse
import os
import sys
import uuid
from datetime import datetime

from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv("/home/debamit007/model-training-loop/.env")

from langchain.chat_models import init_chat_model

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

chat_model = None

if MINIMAX_API_KEY:
    os.environ["ANTHROPIC_BASE_URL"] = "https://api.minimax.io/anthropic"
    os.environ["ANTHROPIC_API_KEY"] = MINIMAX_API_KEY
    chat_model = init_chat_model(model="MiniMax-M2.5", model_provider="anthropic")
    print("Using MiniMax API (Anthropic-compatible)")
elif ANTHROPIC_API_KEY:
    os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
    chat_model = init_chat_model(
        model="claude-sonnet-4-5-20250929", model_provider="anthropic"
    )
    print("Using Anthropic API")
elif OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    chat_model = init_chat_model(model="gpt-4o", model_provider="openai")
    print("Using OpenAI API")
else:
    print(
        "Warning: No API key found. Set MINIMAX_API_KEY, ANTHROPIC_API_KEY, or OPENAI_API_KEY"
    )


from deepagents import create_deep_agent
from agent.logging_middleware import (
    log_goal,
    log_step,
    complete_journey,
    get_current_session,
)
from agent.country_tool import get_country_info
from agent.schema_logging_middleware import SchemaLoggingMiddleware
from logger import AgentLogger


def detect_goal_type(user_input: str) -> str:
    """Detect the goal type from user input."""
    user_lower = user_input.lower()

    if "pay" in user_lower or "payment" in user_lower or "bill" in user_lower:
        return "payment"
    elif "travel" in user_lower or "trip" in user_lower or "flight" in user_lower:
        return "travel"
    elif "research" in user_lower or "find" in user_lower or "search" in user_lower:
        return "research"
    else:
        return "general"


def create_agent(checkpointer=None):
    """Create a deep agent with logging tools."""
    system_prompt = """You are a helpful personal AI assistant. 

When the user tells you something they want to do (like "pay my bill", "plan a trip", "research something"):
1. First, use the log_goal tool to log their goal with the appropriate goal_type
2. Then proceed to help them
3. Use log_step to track important steps in helping them
4. When done, use complete_journey to finish

Goal types:
- payment: for anything related to payments, bills, finances
- travel: for trip planning, flights, hotels
- research: for information gathering, searches
- general: for everything else

For travel planning, use the get_country_info tool to get country details like capital, population, languages, currencies, etc.

Always be helpful and friendly. Use available tools (read_file, write_file, etc.) to assist the user."""

    schema_middleware = SchemaLoggingMiddleware()

    agent = create_deep_agent(
        system_prompt=system_prompt,
        checkpointer=checkpointer,
        model=chat_model,
        tools=[
            log_goal,
            log_step,
            complete_journey,
            get_current_session,
            get_country_info,
        ],
        middleware=[schema_middleware],
    )

    return agent


def run_interactive(agent, checkpointer, storage_path):
    """Run an interactive chat session."""
    session_id = str(uuid.uuid4())[:8]
    config = {"configurable": {"thread_id": session_id}}

    logger = AgentLogger(storage_path=storage_path)

    print(f"=== New Session Started ===")
    print(f"Session ID: {session_id}")
    print(f"Type 'quit' or 'exit' to end the session")
    print(f"Type 'history' to see conversation so far")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit"]:
                print("Session ended.")
                break

            if user_input.lower() == "history":
                state = agent.get_state(config)
                if state and state.values.get("messages"):
                    print("\n=== Conversation History ===")
                    for msg in state.values["messages"]:
                        role = (
                            msg.type
                            if hasattr(msg, "type")
                            else msg.get("type", "unknown")
                        )
                        if role == "human":
                            print(f"You: {msg.content}")
                        elif role == "ai":
                            print(f"Assistant: {msg.content}")
                    print("=== End History ===\n")
                continue

            if not user_input:
                continue

            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config=config,
            )

            response = result["messages"][-1].content

            print(f"\nAssistant: {response}\n")

        except KeyboardInterrupt:
            print("\nSession interrupted.")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

    return session_id


def run_single_query(agent, checkpointer, user_input, storage_path):
    """Run a single query (one-shot mode)."""
    session_id = str(uuid.uuid4())[:8]
    config = {"configurable": {"thread_id": session_id}}

    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config,
    )

    response = result["messages"][-1].content

    print("\n=== AGENT RESPONSE ===")
    print(response)
    print("\n=== JOURNEY COMPLETE ===")
    print(f"Session ID: {session_id}")

    return session_id


def list_sessions(checkpointer):
    """List all available sessions."""
    print("=== Available Sessions ===")
    print("(In-memory - only shows current process sessions)")
    print()
    print("Use --session-id to resume a session")
    print("Use --new-session to start a fresh session")


def main():
    parser = argparse.ArgumentParser(
        description="Personal AI Agent CLI - Multi-turn conversation with DeepAgents"
    )
    parser.add_argument(
        "query",
        nargs="?",
        type=str,
        help="Your request to the agent (omit for interactive mode)",
    )
    parser.add_argument(
        "--session-id", type=str, help="Resume an existing session by ID"
    )
    parser.add_argument(
        "--new-session",
        action="store_true",
        help="Start a new session (generates new session ID)",
    )
    parser.add_argument(
        "--list-sessions", action="store_true", help="List available sessions"
    )
    parser.add_argument(
        "--storage",
        type=str,
        default="weights_n_biases.json",
        help="Path to storage file (default: weights_n_biases.json)",
    )

    args = parser.parse_args()

    checkpointer = InMemorySaver()

    if args.list_sessions:
        list_sessions(checkpointer)
        return

    if args.session_id:
        print(f"Resuming session: {args.session_id}")

    agent = create_agent(checkpointer=checkpointer)

    if args.session_id:
        print(f"Resuming session: {args.session_id}")
        config = {"configurable": {"thread_id": args.session_id}}

        user_input = args.query or input("You: ").strip()

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )

        response = result["messages"][-1].content
        print(f"\nAssistant: {response}\n")

    elif args.query:
        run_single_query(agent, checkpointer, args.query, args.storage)

    else:
        run_interactive(agent, checkpointer, args.storage)


if __name__ == "__main__":
    main()
