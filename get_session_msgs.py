#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/debamit007/model-training-loop')

from agent.conversation_analyzer import get_session_messages
import json

msgs = get_session_messages('b7a8bfbd')
print(f"Found {len(msgs)} messages\n")

for i, msg in enumerate(msgs):
    print(f"=== Message {i+1} ===")
    print(json.dumps(msg, indent=2))
    print()
