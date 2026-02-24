import sqlite3
import json

conn = sqlite3.connect('/home/debamit007/model-training-loop/sessions/checkpoints.db')
cur = conn.cursor()
cur.execute("SELECT checkpoint FROM checkpoints WHERE thread_id = 'b7a8bfbd' ORDER BY checkpoint_id")
for row in cur.fetchall():
    data = json.loads(row[0])
    if 'messages' in data.get('channel_values', {}):
        for msg in data['channel_values']['messages']:
            print(msg)
