import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with the required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table for storing typing test results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS typing_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                wpm REAL NOT NULL,
                accuracy REAL NOT NULL,
                mistakes INTEGER NOT NULL,
                duration REAL NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_test_result(self, difficulty, wpm, accuracy, mistakes, duration):
        """Save a typing test result to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO typing_tests (date, difficulty, wpm, accuracy, mistakes, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), difficulty, wpm, accuracy, mistakes, duration))
        
        conn.commit()
        conn.close()
    
    def get_test_history(self):
        """Retrieve all typing test results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM typing_tests ORDER BY date DESC')
        results = cursor.fetchall()
        
        conn.close()
        return results
    
    def get_average_stats(self, difficulty=None):
        """Get average statistics, optionally filtered by difficulty"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if difficulty:
            cursor.execute('''
                SELECT AVG(wpm), AVG(accuracy), AVG(mistakes) 
                FROM typing_tests 
                WHERE difficulty = ?
            ''', (difficulty,))
        else:
            cursor.execute('''
                SELECT AVG(wpm), AVG(accuracy), AVG(mistakes) 
                FROM typing_tests
            ''')
        
        result = cursor.fetchone()
        conn.close()
        return result