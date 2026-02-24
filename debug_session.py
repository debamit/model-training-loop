#!/usr/bin/env python3
import sqlite3
import pickle

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
            print(f"=== Checkpoint: {checkpoint_id} ===")
            print(f"Keys: {data.keys() if isinstance(data, dict) else type(data)}")
            if isinstance(data, dict):
                for k, v in data.items():
                    if k != 'messages':
                        print(f"  {k}: {str(v)[:200]}")
            print()
        except Exception as e:
            print(f"Checkpoint {checkpoint_id}: Error - {e}")
            print()

conn.close()
