import sqlite3
import hashlib
import os
import logging
from datetime import datetime
import json
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.db_path = 'fitness_app.db'
        self.conn = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Create a database connection with proper settings"""
        try:
            # Ensure the database directory exists
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON")
            logger.info(f"Connected to database at {self.db_path}")
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            raise

    def _create_tables(self):
        """Create all required tables if they don't exist"""
        try:
            cursor = self.conn.cursor()
            
            # Create users table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                password_hash TEXT NOT NULL,
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
            
            # Create other tables...
            cursor.execute('''
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
            
            cursor.execute('''
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
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
            raise

    def __del__(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

def get_db():
    """Get a database connection"""
    try:
        conn = sqlite3.connect('fitness_app.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except Exception as e:
        logger.error(f"Error creating database connection: {str(e)}")
        raise

def reset_database():
    """Reset the database by removing the file and recreating it"""
    try:
        # Close any existing connections
        if os.path.exists('fitness_app.db'):
            os.remove('fitness_app.db')
            logger.info("Removed existing database file")
        
        # Create new database
        db = DatabaseManager()
        logger.info("Database reset complete")
        return True
    except Exception as e:
        logger.error(f"Error resetting database: {str(e)}")
        return False

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_username(username):
    """Validate username format"""
    if not username or not isinstance(username, str):
        return False, "Username is required"
    if not 3 <= len(username) <= 20:
        return False, "Username must be between 3 and 20 characters"
    if not re.match("^[a-zA-Z0-9_-]+$", username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    return True, "Valid username"

def create_user(username, name, password, email=None, weight=None, height=None, age=None, 
                gender=None, fitness_goal=None, activity_level=None):
    """
    Create a new user with proper validation and error handling
    Returns: (success: bool, message: str)
    """
    logger.info(f"Attempting to create user: {username}")
    
    # Input validation
    if not username or not isinstance(username, str):
        return False, "Username is required"
    if not 3 <= len(username) <= 20:
        return False, "Username must be between 3 and 20 characters"
    if not username.replace('-', '').replace('_', '').isalnum():
        return False, "Username can only contain letters, numbers, hyphens, and underscores"
    
    if not name or not isinstance(name, str):
        return False, "Name is required"
    
    if not password or not isinstance(password, str):
        return False, "Password is required"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if username exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return False, "Username already exists"
        
        # Create user with transaction
        try:
            conn.execute("BEGIN TRANSACTION")
            
            # Hash password
            password_hash = hash_password(password)
            
            # Insert user
            cursor.execute('''
                INSERT INTO users (
                    username, name, email, password_hash,
                    height, weight, age, gender,
                    fitness_goal, activity_level
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                username, name, email, password_hash,
                height, weight, age, gender,
                fitness_goal, activity_level
            ))
            
            user_id = cursor.lastrowid
            
            # Verify user was created
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            if not cursor.fetchone():
                raise Exception("User creation verification failed")
            
            conn.commit()
            logger.info(f"Successfully created user: {username} (ID: {user_id})")
            return True, "Account created successfully"
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Error during user creation: {str(e)}")
            raise
            
    except sqlite3.IntegrityError as e:
        if conn:
            conn.rollback()
        logger.error(f"Database integrity error: {str(e)}")
        return False, "Username already exists"
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error creating user: {str(e)}")
        return False, f"Error creating account: {str(e)}"
    finally:
        if conn:
            conn.close()

def verify_user(username, password):
    """
    Verify user credentials
    Returns: (success: bool, result: dict or str)
    """
    logger.info(f"Verifying user: {username}")
    
    if not username or not password:
        return False, "Username and password are required"
    
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get user
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if not user:
            logger.info(f"No user found with username: {username}")
            return False, "Invalid username or password"
        
        # Verify password
        if user['password_hash'] != hash_password(password):
            logger.info(f"Password verification failed for user: {username}")
            return False, "Invalid username or password"
        
        # Return user data without sensitive information
        user_dict = dict(user)
        user_dict.pop('password_hash', None)
        logger.info(f"Successfully verified user: {username}")
        return True, user_dict
        
    except Exception as e:
        logger.error(f"Error verifying user: {str(e)}")
        return False, f"Error during verification: {str(e)}"
    finally:
        if conn:
            conn.close()

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        if user:
            user_dict = dict(user)
            user_dict.pop('password_hash', None)
            return user_dict
        return None
    finally:
        if conn:
            conn.close()

def update_user_profile(user_id, data):
    """Update user profile information"""
    conn = get_db()
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
    
    return get_user_by_id(user_id)

def log_workout(user_id, workout_data):
    """Log a workout session"""
    conn = get_db()
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
    conn = get_db()
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
    conn = get_db()
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
    conn = get_db()
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

def get_user_by_username(username):
    """Get user by username"""
    logger.info(f"Fetching user by username: {username}")
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            user_dict = dict(user)
            user_dict.pop('password_hash', None)  # Remove sensitive data
            return user_dict
        logger.info(f"No user found with username: {username}")
        return None
    except Exception as e:
        logger.error(f"Error fetching user by username: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()

# Reset and reinitialize the database when the module is imported
# reset_database() 