import sqlite3
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('fitness_data.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS nutrition_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            date TEXT,
            food_name TEXT,
            meal_type TEXT,
            serving_size REAL,
            calories REAL,
            protein REAL,
            carbs REAL,
            fat REAL,
            fiber REAL
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fat REAL,
            date_modified TEXT
        )
        ''')
        self.conn.commit()

    def add_food_log(self, log_entry):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO nutrition_logs (time, date, food_name, meal_type, serving_size, 
                                  calories, protein, carbs, fat, fiber)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            log_entry['time'],
            log_entry['date'].isoformat() if isinstance(log_entry['date'], datetime) else log_entry['date'],
            log_entry['food_name'],
            log_entry['meal_type'],
            log_entry['serving_size'],
            log_entry['calories'],
            log_entry['protein'],
            log_entry['carbs'],
            log_entry['fat'],
            log_entry['fiber']
        ))
        self.conn.commit()

    def get_logs_by_date(self, date):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT * FROM nutrition_logs WHERE date = ?
        ''', (date.isoformat() if isinstance(date, datetime) else date,))
        
        columns = [description[0] for description in cursor.description]
        logs = []
        for row in cursor.fetchall():
            log_dict = dict(zip(columns, row))
            logs.append(log_dict)
        return logs

    def clear_logs_by_date(self, date):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM nutrition_logs WHERE date = ?', 
                      (date.isoformat() if isinstance(date, datetime) else date,))
        self.conn.commit()

    def save_daily_goals(self, goals):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO daily_goals (id, calories, protein, carbs, fat, date_modified)
        VALUES (1, ?, ?, ?, ?, ?)
        ''', (goals['calories'], goals['protein'], goals['carbs'], goals['fat'], 
              datetime.now().isoformat()))
        self.conn.commit()

    def get_daily_goals(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT calories, protein, carbs, fat FROM daily_goals WHERE id = 1')
        row = cursor.fetchone()
        if row:
            return {
                'calories': row[0],
                'protein': row[1],
                'carbs': row[2],
                'fat': row[3]
            }
        return None

    def __del__(self):
        self.conn.close() 