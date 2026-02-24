#!/usr/bin/env python3
import sqlite3
import base64
import pickle
import json

conn = sqlite3.connect("/home/debamit007/model-training-loop/sessions/checkpoints.db")
cur = conn.cursor()

# Check the writes table for messages
cur.execute("""
    SELECT channel, type, value 
    FROM writes 
    WHERE thread_id = 'b7a8bfbd'
    ORDER BY checkpoint_id ASC, idx ASC
""")

results = cur.fetchall()
print(f"Found {len(results)} write records for session b7a8bfbd\n")

for channel, type_val, value_blob in results:
    if value_blob:
        try:
            data = pickle.loads(value_blob)
            if isinstance(data, dict) and 'messages' in data:
                messages = data['messages']
                print(f"=== Channel: {channel} ===")
                for msg in messages:
                    msg_type = type(msg).__name__
                    content = getattr(msg, 'content', '')[:300] if hasattr(msg, 'content') else str(msg)[:300]
                    print(f"  [{msg_type}]: {content}")
                print()
            elif isinstance(data, list):
                print(f"=== Channel: {channel} (list) ===")
                for msg in data:
                    msg_type = type(msg).__name__
                    content = getattr(msg, 'content', '')[:300] if hasattr(msg, 'content') else str(msg)[:300]
                    print(f"  [{msg_type}]: {content}")
                print()
        except Exception as e:
            print(f"Could not parse: {e}")

conn.close()
