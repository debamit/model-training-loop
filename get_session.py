#!/usr/bin/env python3
import sqlite3
import base64
import pickle
import json

conn = sqlite3.connect("/home/debamit007/model-training-loop/sessions/checkpoints.db")
cur = conn.cursor()

cur.execute("""
    SELECT checkpoint_id, checkpoint, metadata 
    FROM checkpoints 
    WHERE thread_id = 'b7a8bfbd'
    ORDER BY checkpoint_id ASC
""")

results = cur.fetchall()
print(f"Found {len(results)} checkpoints for session b7a8bfbd\n")

for checkpoint_id, checkpoint_blob, metadata_blob in results:
    if checkpoint_blob:
        try:
            data = pickle.loads(checkpoint_blob)
            if isinstance(data, dict) and 'messages' in data:
                messages = data['messages']
                print(f"=== Checkpoint: {checkpoint_id} ===")
                for msg in messages:
                    msg_type = type(msg).__name__
                    content = getattr(msg, 'content', '')[:200] if hasattr(msg, 'content') else str(msg)[:200]
                    print(f"  [{msg_type}]: {content}")
                print()
        except Exception as e:
            pass  # Skip checkpoints that don't have message data

conn.close()
