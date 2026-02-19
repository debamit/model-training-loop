import argparse
import sys
from agent import AgentOrchestrator


def main():
    parser = argparse.ArgumentParser(
        description="Personal AI Agent CLI - Test goal & journey logging"
    )
    parser.add_argument("query", type=str, help="Your request to the agent")
    parser.add_argument(
        "--storage",
        type=str,
        default="weights_n_biases.json",
        help="Path to storage file (default: weights_n_biases.json)",
    )

    args = parser.parse_args()

    orchestrator = AgentOrchestrator(storage_path=args.storage)
    result = orchestrator.run(user_input=args.query)

    print("\n=== AGENT RESPONSE ===")
    print(result.get("response", "No response"))
    print("\n=== JOURNEY COMPLETE ===")
    print(f"Journey ID: {result.get('journey_id')}")
    print(f"Goal ID: {result.get('goal_id')}")
    print(f"Steps logged: {result.get('step_count')}")


if __name__ == "__main__":
    main()
