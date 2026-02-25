import sqlite3
import json
import os

DB_FILE = 'analysis.db'

def init_db():
    """Initialize the SQLite database for job tracking."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs
                 (id TEXT PRIMARY KEY, status TEXT, result TEXT, filename TEXT)''')
    conn.commit()
    conn.close()

def create_job(job_id: str, filename: str):
    """Create a new job in the queue."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO jobs (id, status, result, filename) VALUES (?, ?, ?, ?)",
              (job_id, "PROCESSING", "", filename))
    conn.commit()
    conn.close()

def update_job(job_id: str, status: str, result: str):
    """Update job status and output."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE jobs SET status=?, result=? WHERE id=?",
              (status, result, job_id))
    conn.commit()
    conn.close()

def get_job(job_id: str):
    """Retrieve job status."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT status, result, filename FROM jobs WHERE id=?", (job_id,))
    row = c.fetchone()
    conn.close()
    return row