# feedback_store.py
# Simple feedback storage for premium feature requests

import sqlite3
import os
from datetime import datetime
from typing import Optional

# Database file path
DB_PATH = 'feedback.db'

def init_feedback_db():
    """Initialize the feedback database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS premium_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_text TEXT NOT NULL,
            email TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id TEXT,
            ip_address TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_feedback(feedback_text: str, email: Optional[str] = None, user_id: Optional[str] = None, ip_address: Optional[str] = None):
    """Save premium feedback to database"""
    try:
        init_feedback_db()  # Ensure table exists
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO premium_feedback (feedback_text, email, user_id, ip_address)
            VALUES (?, ?, ?, ?)
        ''', (feedback_text, email, user_id, ip_address))
        
        conn.commit()
        feedback_id = cursor.lastrowid
        conn.close()
        
        return feedback_id
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return None

def get_all_feedback():
    """Get all feedback entries (for admin use)"""
    try:
        if not os.path.exists(DB_PATH):
            return []
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, feedback_text, email, timestamp, user_id, ip_address
            FROM premium_feedback
            ORDER BY timestamp DESC
        ''')
        
        feedback_list = cursor.fetchall()
        conn.close()
        
        return feedback_list
    except Exception as e:
        print(f"Error getting feedback: {e}")
        return []

def get_feedback_count():
    """Get total number of feedback entries"""
    try:
        if not os.path.exists(DB_PATH):
            return 0
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM premium_feedback')
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    except Exception as e:
        print(f"Error getting feedback count: {e}")
        return 0