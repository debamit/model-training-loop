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
    get_session_date,
    load_existing_analysis,
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


def analyze_session(session_ids: list[str], output_dir: str = DEFAULT_OUTPUT_DIR):
    """Analyze one or more sessions, merging with existing analysis by date."""
    if not session_ids:
        print("No session IDs provided.")
        return

    print(f"Analyzing session(s): {', '.join(session_ids)}")

    sessions_by_date = {}
    for session_id in session_ids:
        session_date = get_session_date(session_id)
        if session_date not in sessions_by_date:
            sessions_by_date[session_date] = []
        sessions_by_date[session_date].append(session_id)

    all_source_sessions = []
    all_goals = []

    for date, date_sessions in sessions_by_date.items():
        existing = load_existing_analysis(date, output_dir)
        existing_goals = existing.goals if existing else None
        existing_sessions = existing.source_sessions if existing else []

        result = analyze_conversations(date_sessions, existing_goals=existing_goals)

        all_source_sessions.extend(existing_sessions)
        all_source_sessions.extend(result.source_sessions)

        for goal in result.goals:
            all_goals.append(goal)

    output_path = (
        Path(output_dir) / f"chat_Analysis_{datetime.now().strftime('%Y-%m-%d')}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "analyzed_at": datetime.now().isoformat(),
        "source_sessions": list(set(all_source_sessions)),
        "goals": [g.model_dump() for g in all_goals],
    }

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2, default=str)

    print(f"Analysis saved to: {output_path}")
    print(f"Total sessions: {len(all_source_sessions)}")
    print(f"Goals found: {len(all_goals)}")

    for goal in all_goals:
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
        "session_ids",
        nargs="*",
        type=str,
        help="Session ID(s) to analyze (multiple allowed)",
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

    if args.session_ids:
        analyze_session(args.session_ids, args.output_dir)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
