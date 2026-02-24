#!/usr/bin/env python3
"""Query session messages from checkpoint database."""
import json
import sqlite3

conn = sqlite3.connect("sessions/checkpoints.db")
cur = conn.cursor()

# Get all messages for session b7a8bfbd
cur.execute("""
    SELECT c.checkpoint_id, c.channel, c.value 
    FROM checkpoints c
    WHERE c.thread_id = 'b7a8bfbd'
    ORDER BY c.checkpoint_id ASC
""")

results = cur.fetchall()
print(f"Found {len(results)} checkpoint records for session b7a8bfbd")
print()

# Parse the checkpoint values to extract messages
import base64
import pickle

for checkpoint_id, channel, value in results:
    if channel == "messages":
        print(f"Channel: {channel}, Checkpoint: {checkpoint_id}")
        try:
            # Try to unpickle the value
            data = pickle.loads(base64.b64decode(value))
            if isinstance(data, list):
                for msg in data:
                    print(f"  {type(msg).__name__}: {getattr(msg, 'content', str(msg))[:100]}")
            else:
                print(f"  Data: {str(data)[:200]}")
        except Exception as e:
            print(f"  Could not parse: {e}")
            print(f"  Raw value: {value[:200] if value else 'None'}...")
        print()

conn.close()
