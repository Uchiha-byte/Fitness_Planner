import sqlite3
from datetime import datetime
import json
import hashlib
import re

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('fitness_app.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create nutrition_logs table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS nutrition_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            time TEXT,
            date TEXT,
            food_name TEXT,
            meal_type TEXT,
            serving_size REAL,
            calories REAL,
            protein REAL,
            carbs REAL,
            fat REAL,
            fiber REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Create daily_goals table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fat REAL,
            date_modified TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
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

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    return conn

def reset_db():
    """Drop all tables and recreate them"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Drop existing tables
    c.execute('DROP TABLE IF EXISTS nutrition_logs')
    c.execute('DROP TABLE IF EXISTS workout_logs')
    c.execute('DROP TABLE IF EXISTS progress_tracking')
    c.execute('DROP TABLE IF EXISTS users')
    
    conn.commit()
    conn.close()
    
    # Reinitialize the database
    init_db()

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create users table with additional fields
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            height REAL,
            weight REAL,
            age INTEGER,
            gender TEXT,
            fitness_goal TEXT,
            activity_level TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create workout_logs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS workout_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            workout_type TEXT,
            duration INTEGER,
            calories_burned INTEGER,
            date DATE,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create nutrition_logs table if not exists (compatible with old schema)
    c.execute('''
        CREATE TABLE IF NOT EXISTS nutrition_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            time TEXT,
            date TEXT,
            food_name TEXT,
            meal_type TEXT,
            serving_size REAL,
            calories REAL,
            protein REAL,
            carbs REAL,
            fat REAL,
            fiber REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create progress_tracking table
    c.execute('''
        CREATE TABLE IF NOT EXISTS progress_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            weight REAL,
            body_fat REAL,
            muscle_mass REAL,
            date DATE,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create daily_goals table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fat REAL,
            date_modified TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_username(username):
    """Validate username format"""
    if not 3 <= len(username) <= 20:
        return False, "Username must be between 3 and 20 characters"
    if not re.match("^[a-zA-Z0-9_-]+$", username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    return True, "Valid username"

def create_user(username, name, email, password, weight=None, height=None, age=None, 
                gender=None, fitness_goal=None, activity_level=None):
    # Validate username
    is_valid, message = validate_username(username)
    if not is_valid:
        return False, message

    conn = get_db_connection()
    c = conn.cursor()
    try:
        # Check if username exists
        c.execute('SELECT id FROM users WHERE username = ?', (username,))
        if c.fetchone():
            return False, "Username already exists"

        # Check if email exists
        c.execute('SELECT id FROM users WHERE email = ?', (email,))
        if c.fetchone():
            return False, "Email already exists"

        password_hash = hash_password(password)
        c.execute('''
            INSERT INTO users 
            (username, name, email, password, weight, height, age, gender, 
             fitness_goal, activity_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, name, email, password_hash, weight, height, age, gender, 
              fitness_goal, activity_level))
        conn.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already exists"
        elif "email" in str(e):
            return False, "Email already exists"
        return False, "An error occurred while creating user"
    finally:
        conn.close()

def verify_user(identifier, password):
    """
    Verify user using either email or username
    :param identifier: email or username
    :param password: user password
    :return: (success, result) tuple
    """
    conn = get_db_connection()
    c = conn.cursor()
    password_hash = hash_password(password)
    
    # Try to find user by email or username
    c.execute('''
        SELECT * FROM users 
        WHERE (email = ? OR username = ?) AND password = ?
    ''', (identifier, identifier, password_hash))
    
    user = c.fetchone()
    conn.close()
    
    if user:
        return True, dict(user)
    return False, "Invalid credentials"

def get_user_by_id(user_id):
    """Get user details by ID"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        SELECT id, username, name, email, height, weight, age, gender, 
               fitness_goal, activity_level, created_at, updated_at
        FROM users 
        WHERE id = ?
    ''', (user_id,))
    
    user = c.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None

def update_user_profile(user_id, data):
    """Update user profile information"""
    conn = get_db_connection()
    c = conn.cursor()
    
    valid_fields = [
        'name', 'height', 'weight', 'age', 'gender',
        'fitness_goal', 'activity_level'
    ]
    
    updates = []
    values = []
    
    for field in valid_fields:
        if field in data:
            updates.append(f"{field} = ?")
            values.append(data[field])
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        values.append(user_id)
        
        c.execute(query, values)
        conn.commit()
    
    conn.close()
    return get_user_by_id(user_id)

def log_workout(user_id, workout_data):
    """Log a workout session"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO workout_logs 
        (user_id, workout_type, duration, calories_burned, date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        workout_data['type'],
        workout_data['duration'],
        workout_data['calories_burned'],
        workout_data.get('date', datetime.now().date()),
        workout_data.get('notes', '')
    ))
    
    conn.commit()
    conn.close()

def log_nutrition(user_id, nutrition_data):
    """Log nutrition information"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Support both old and new nutrition logging formats
    if 'food_items' in nutrition_data:
        # New format
        c.execute('''
            INSERT INTO nutrition_logs 
            (user_id, meal_type, food_items, calories, protein, carbs, fats, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            nutrition_data['meal_type'],
            json.dumps(nutrition_data['food_items']),
            nutrition_data['calories'],
            nutrition_data['protein'],
            nutrition_data['carbs'],
            nutrition_data['fats'],
            nutrition_data.get('date', datetime.now().date())
        ))
    else:
        # Old format
        c.execute('''
            INSERT INTO nutrition_logs 
            (user_id, time, date, food_name, meal_type, serving_size, 
             calories, protein, carbs, fat, fiber)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            nutrition_data.get('time', datetime.now().strftime('%H:%M')),
            nutrition_data.get('date', datetime.now().date()),
            nutrition_data.get('food_name', ''),
            nutrition_data['meal_type'],
            nutrition_data.get('serving_size', 1.0),
            nutrition_data['calories'],
            nutrition_data['protein'],
            nutrition_data['carbs'],
            nutrition_data['fat'],
            nutrition_data.get('fiber', 0.0)
        ))
    
    conn.commit()
    conn.close()

def track_progress(user_id, progress_data):
    """Track user progress metrics"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO progress_tracking 
        (user_id, weight, body_fat, muscle_mass, date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        progress_data['weight'],
        progress_data.get('body_fat'),
        progress_data.get('muscle_mass'),
        progress_data.get('date', datetime.now().date()),
        progress_data.get('notes', '')
    ))
    
    conn.commit()
    conn.close()

def get_user_stats(user_id):
    """Get user statistics and progress"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get latest progress tracking
    c.execute('''
        SELECT * FROM progress_tracking 
        WHERE user_id = ? 
        ORDER BY date DESC 
        LIMIT 1
    ''', (user_id,))
    latest_progress = c.fetchone()
    
    # Get workout summary for the current week
    c.execute('''
        SELECT COUNT(*) as workout_count, 
               SUM(duration) as total_duration,
               SUM(calories_burned) as total_calories
        FROM workout_logs 
        WHERE user_id = ? 
        AND date >= date('now', '-7 days')
    ''', (user_id,))
    workout_summary = c.fetchone()
    
    # Get nutrition summary for today
    c.execute('''
        SELECT SUM(calories) as total_calories,
               SUM(protein) as total_protein,
               SUM(carbs) as total_carbs,
               SUM(fat) as total_fats
        FROM nutrition_logs 
        WHERE user_id = ? 
        AND date = date('now')
    ''', (user_id,))
    nutrition_summary = c.fetchone()
    
    conn.close()
    
    return {
        'progress': dict(latest_progress) if latest_progress else None,
        'workouts': dict(workout_summary) if workout_summary else None,
        'nutrition': dict(nutrition_summary) if nutrition_summary else None
    }

# Reset and reinitialize the database when the module is imported
reset_db() 