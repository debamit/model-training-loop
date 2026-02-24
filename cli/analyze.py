import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("/home/debamit007/model-training-loop/.env")

from config import create_chat_model
from agent.conversation_analyzer import (
    analyze_conversations,
    get_all_sessions,
    get_session_messages,
)


DEFAULT_OUTPUT_DIR = "./analysis"


def list_sessions():
    """List all available session IDs."""
    sessions = get_all_sessions()

    if not sessions:
        print("No sessions found.")
        return

    print("=== Available Sessions ===")
    for session_id in sessions:
        messages = get_session_messages(session_id)
        msg_count = len(messages)
        print(f"  {session_id} ({msg_count} messages)")
    print()


def analyze_session(session_id: str, output_dir: str = DEFAULT_OUTPUT_DIR):
    """Analyze a single session."""
    print(f"Analyzing session: {session_id}")

    result = analyze_conversations([session_id])

    output_path = Path(output_dir) / f"chat_Analysis_{result.date}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(result.model_dump(), f, indent=2, default=str)

    print(f"Analysis saved to: {output_path}")
    print(f"Goals found: {len(result.goals)}")

    for goal in result.goals:
        print(f"  - {goal.goal}: {len(goal.conversations)} conversation(s)")


def analyze_day(day: str, output_dir: str = DEFAULT_OUTPUT_DIR):
    """Analyze all sessions from a particular day."""
    print(f"Analyzing sessions from: {day}")

    sessions = get_all_sessions()

    if not sessions:
        print("No sessions found.")
        return

    result = analyze_conversations(sessions)

    output_path = Path(output_dir) / f"chat_Analysis_{day}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(result.model_dump(), f, indent=2, default=str)

    print(f"Analysis saved to: {output_path}")
    print(f"Sessions analyzed: {len(result.source_sessions)}")
    print(f"Goals found: {len(result.goals)}")

    for goal in result.goals:
        print(f"  - {goal.goal}: {len(goal.conversations)} conversation(s)")


def analyze_all(output_dir: str = DEFAULT_OUTPUT_DIR):
    """Analyze all sessions."""
    print("Analyzing all sessions")

    sessions = get_all_sessions()

    if not sessions:
        print("No sessions found.")
        return

    result = analyze_conversations(sessions)

    today = datetime.now().strftime("%Y-%m-%d")
    output_path = Path(output_dir) / f"chat_Analysis_{today}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(result.model_dump(), f, indent=2, default=str)

    print(f"Analysis saved to: {output_path}")
    print(f"Sessions analyzed: {len(result.source_sessions)}")
    print(f"Goals found: {len(result.goals)}")

    for goal in result.goals:
        print(f"  - {goal.goal}: {len(goal.conversations)} conversation(s)")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze conversations and group by goals"
    )

    parser.add_argument(
        "session_id",
        nargs="?",
        type=str,
        help="Session ID to analyze",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available session IDs",
    )
    parser.add_argument(
        "--day",
        type=str,
        help="Analyze all sessions from a particular day (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Analyze all sessions",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Override model name from config",
    )
    parser.add_argument(
        "--provider",
        type=str,
        help="Override provider from config (minimax, anthropic, openai)",
    )

    args = parser.parse_args()

    if args.list:
        list_sessions()
        return

    if args.day:
        analyze_day(args.day, args.output_dir)
        return

    if args.all:
        analyze_all(args.output_dir)
        return

    if args.session_id:
        analyze_session(args.session_id, args.output_dir)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
