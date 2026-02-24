#!/usr/bin/env python3
import sqlite3
conn = sqlite3.connect("/home/debamit007/model-training-loop/sessions/checkpoints.db")
cur = conn.cursor()
cur.execute("SELECT sql FROM sqlite_master WHERE type='table'")
print(cur.fetchall())
conn.close()
