import argparse
import json
import os
import sys
import uuid
from datetime import datetime

from dotenv import load_dotenv

load_dotenv("/home/debamit007/model-training-loop/.env")

from config import create_chat_model
from deepagents import create_deep_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from agent.country_tool import get_country_info


def export_messages(agent, config, filepath: str):
    """Export messages to a JSON file."""
    state = agent.get_state(config)
    if not state or not state.values.get("messages"):
        print("No messages to export")
        return

    messages = []
    for msg in state.values["messages"]:
        if isinstance(msg, str):
            msg_dict = {
                "type": "unknown",
                "content": msg,
            }
        else:
            msg_dict = {
                "type": msg.type,
                "content": msg.content,
            }
            if hasattr(msg, "name") and msg.name:
                msg_dict["name"] = msg.name
            if hasattr(msg, "tool_call_id") and msg.tool_call_id:
                msg_dict["tool_call_id"] = msg.tool_call_id
        messages.append(msg_dict)

    with open(filepath, "w") as f:
        json.dump(messages, f, indent=2, default=str)
    print(f"Messages exported to {filepath}")


def create_agent(checkpointer=None, chat_model=None):
    """Create a deep agent."""
    if chat_model is None:
        from config import create_chat_model

        chat_model = create_chat_model()
    system_prompt = """You are a helpful personal AI assistant.

## IMPORTANT: Always check available skills first

Before responding to ANY user request:
1. Check if a skill matches the user's intent by looking at skill triggers
2. If a skill matches, use ONLY that skill to complete the task
3. If no skill matches, then answer directly using your knowledge

## Available Skills

- api-goal-mapper: Map API endpoints to user goals
- api-goal-saver: Save API goals to JSON
- api-spec-finder: Find API specification files
- api-spec-reader: Read API specification files
- bot-simulation: Simulate conversations with bots
- pdf-finder: Find PDF files
- pdf-goal-mapper: Map PDF content to user goals
- pdf-goal-saver: Save PDF goals to JSON
- pdf-reader: Extract text from PDF files
- skill-author: Help create new skills

## Skill Workflow

For multi-step tasks (e.g., "extract goals from pdf"):
1. Call finder skill → locate the file
2. Call reader skill → extract content
3. Call goal-mapper skill → extract goals
4. Call saver skill → save to file
5. Present result to user

## Tools

For travel queries, use get_country_info tool.

Always be helpful and stick to available skills."""

    agent = create_deep_agent(
        system_prompt=system_prompt,
        checkpointer=checkpointer,
        model=chat_model,
        tools=[
            get_country_info,
        ],
    )

    return agent


def run_interactive(agent, checkpointer, export_filepath=None):
    """Run an interactive chat session."""
    session_id = str(uuid.uuid4())[:8]
    config = {"configurable": {"thread_id": session_id}}

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
                if export_filepath:
                    export_messages(agent, config, export_filepath)
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


def run_single_query(agent, checkpointer, user_input, export_filepath=None):
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

    if export_filepath:
        export_messages(agent, config, export_filepath)

    return session_id

    return session_id


def list_sessions(checkpointer):
    """List all available sessions."""
    print("=== Available Sessions ===")
    threads = checkpointer.list_all_threads()
    if not threads:
        print("No sessions found.")
        print("Use --new-session to start a fresh session")
        return
    for thread in threads:
        print(f"Session ID: {thread['thread_id']}")
        print(f"  Checkpoints: {thread['num_checkpoints']}")
        if thread.get("last_checkpoint"):
            print(
                f"  Last updated: {thread['last_checkpoint'].get('created_at', 'unknown')}"
            )
        print()


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
        "--no-export",
        action="store_true",
        help="Disable auto-export of conversation to conversation.json",
    )
    parser.add_argument(
        "--export-messages",
        nargs="?",
        const="conversation.json",
        metavar="FILE",
        help="Export messages to JSON file (default: conversation.json)",
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Override model name from config",
    )
    parser.add_argument(
        "--provider",
        type=str,
        help="Override provider from config (minimax, anthropic, openai, custom)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Override API key from config",
    )
    parser.add_argument(
        "--api-base",
        type=str,
        help="Override API base URL (for custom provider)",
    )

    args = parser.parse_args()

    with SqliteSaver.from_conn_string("sessions/checkpoints.db") as checkpointer:
        export_filepath = None if args.no_export else "conversation.json"

        chat_model = create_chat_model(
            model=args.model,
            provider=args.provider,
            api_key=args.api_key,
            api_base=args.api_base,
        )

        agent = create_agent(checkpointer=checkpointer, chat_model=chat_model)

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

            if export_filepath:
                export_messages(agent, config, export_filepath)

        elif args.query:
            run_single_query(agent, checkpointer, args.query, export_filepath)

        else:
            run_interactive(agent, checkpointer, export_filepath)


if __name__ == "__main__":
    main()
