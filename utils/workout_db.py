import sqlite3
from datetime import datetime
import json

class WorkoutDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('fitness_data.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Exercise Library Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            muscle_group TEXT,
            equipment TEXT,
            difficulty TEXT,
            instructions TEXT,
            video_url TEXT,
            is_custom BOOLEAN DEFAULT 0
        )
        ''')

        # Workout Programs Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_date TEXT,
            last_modified TEXT,
            frequency TEXT,
            duration_weeks INTEGER,
            difficulty TEXT,
            tags TEXT
        )
        ''')

        # Workout Days Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_days (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_id INTEGER,
            day_number INTEGER,
            name TEXT,
            FOREIGN KEY (program_id) REFERENCES workout_programs (id)
        )
        ''')

        # Workout Exercises Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_day_id INTEGER,
            exercise_id INTEGER,
            sets INTEGER,
            reps TEXT,
            rest_seconds INTEGER,
            notes TEXT,
            order_in_workout INTEGER,
            is_superset BOOLEAN DEFAULT 0,
            superset_group INTEGER,
            FOREIGN KEY (workout_day_id) REFERENCES workout_days (id),
            FOREIGN KEY (exercise_id) REFERENCES exercises (id)
        )
        ''')

        # Workout Logs Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            start_time TEXT,
            end_time TEXT,
            program_id INTEGER,
            day_id INTEGER,
            notes TEXT,
            rating INTEGER,
            FOREIGN KEY (program_id) REFERENCES workout_programs (id),
            FOREIGN KEY (day_id) REFERENCES workout_days (id)
        )
        ''')

        # Exercise Logs Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercise_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_log_id INTEGER,
            exercise_id INTEGER,
            set_number INTEGER,
            reps INTEGER,
            weight REAL,
            rpe INTEGER,
            notes TEXT,
            FOREIGN KEY (workout_log_id) REFERENCES workout_logs (id),
            FOREIGN KEY (exercise_id) REFERENCES exercises (id)
        )
        ''')

        # Progress Photos Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress_photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            photo_path TEXT,
            notes TEXT
        )
        ''')

        # Body Measurements Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS body_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            weight REAL,
            body_fat REAL,
            chest REAL,
            waist REAL,
            hips REAL,
            biceps REAL,
            thighs REAL,
            notes TEXT
        )
        ''')

        self.conn.commit()

    def add_exercise(self, exercise_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO exercises (name, description, muscle_group, equipment, 
                             difficulty, instructions, video_url, is_custom)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            exercise_data['name'],
            exercise_data.get('description', ''),
            exercise_data.get('muscle_group', ''),
            exercise_data.get('equipment', ''),
            exercise_data.get('difficulty', 'intermediate'),
            exercise_data.get('instructions', ''),
            exercise_data.get('video_url', ''),
            exercise_data.get('is_custom', False)
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_exercises(self, muscle_group=None, equipment=None):
        cursor = self.conn.cursor()
        query = 'SELECT * FROM exercises'
        params = []
        
        if muscle_group or equipment:
            query += ' WHERE'
            if muscle_group:
                query += ' muscle_group = ?'
                params.append(muscle_group)
            if equipment:
                if muscle_group:
                    query += ' AND'
                query += ' equipment = ?'
                params.append(equipment)
        
        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def create_workout_program(self, program_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO workout_programs (name, description, created_date, last_modified,
                                    frequency, duration_weeks, difficulty, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            program_data['name'],
            program_data.get('description', ''),
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            program_data.get('frequency', ''),
            program_data.get('duration_weeks', 4),
            program_data.get('difficulty', 'intermediate'),
            json.dumps(program_data.get('tags', []))
        ))
        self.conn.commit()
        return cursor.lastrowid

    def add_workout_day(self, program_id, day_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO workout_days (program_id, day_number, name)
        VALUES (?, ?, ?)
        ''', (program_id, day_data['day_number'], day_data['name']))
        self.conn.commit()
        return cursor.lastrowid

    def add_workout_exercise(self, day_id, exercise_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO workout_exercises (workout_day_id, exercise_id, sets, reps,
                                     rest_seconds, notes, order_in_workout,
                                     is_superset, superset_group)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            day_id,
            exercise_data['exercise_id'],
            exercise_data['sets'],
            json.dumps(exercise_data['reps']),
            exercise_data.get('rest_seconds', 60),
            exercise_data.get('notes', ''),
            exercise_data['order_in_workout'],
            exercise_data.get('is_superset', False),
            exercise_data.get('superset_group', None)
        ))
        self.conn.commit()

    def log_workout(self, workout_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO workout_logs (date, start_time, end_time, program_id,
                                day_id, notes, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            workout_data['date'],
            workout_data['start_time'],
            workout_data['end_time'],
            workout_data.get('program_id'),
            workout_data.get('day_id'),
            workout_data.get('notes', ''),
            workout_data.get('rating', None)
        ))
        log_id = cursor.lastrowid
        self.conn.commit()
        return log_id

    def log_exercise_set(self, log_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO exercise_logs (workout_log_id, exercise_id, set_number,
                                 reps, weight, rpe, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            log_data['workout_log_id'],
            log_data['exercise_id'],
            log_data['set_number'],
            log_data['reps'],
            log_data['weight'],
            log_data.get('rpe'),
            log_data.get('notes', '')
        ))
        self.conn.commit()

    def add_progress_photo(self, photo_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO progress_photos (date, photo_path, notes)
        VALUES (?, ?, ?)
        ''', (
            photo_data['date'],
            photo_data['photo_path'],
            photo_data.get('notes', '')
        ))
        self.conn.commit()

    def add_body_measurements(self, measurement_data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO body_measurements (date, weight, body_fat, chest, waist,
                                     hips, biceps, thighs, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            measurement_data['date'],
            measurement_data.get('weight'),
            measurement_data.get('body_fat'),
            measurement_data.get('chest'),
            measurement_data.get('waist'),
            measurement_data.get('hips'),
            measurement_data.get('biceps'),
            measurement_data.get('thighs'),
            measurement_data.get('notes', '')
        ))
        self.conn.commit()

    def get_workout_programs(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM workout_programs')
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_workout_days(self, program_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM workout_days WHERE program_id = ?', (program_id,))
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_workout_exercises(self, day_id):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT we.*, e.name, e.muscle_group, e.equipment
        FROM workout_exercises we
        JOIN exercises e ON we.exercise_id = e.id
        WHERE we.workout_day_id = ?
        ORDER BY we.order_in_workout
        ''', (day_id,))
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def delete_program(self, program_id):
        """Delete a workout program and all related data."""
        cursor = self.conn.cursor()
        
        # First, get all workout days for this program
        cursor.execute('SELECT id FROM workout_days WHERE program_id = ?', (program_id,))
        day_ids = [row[0] for row in cursor.fetchall()]
        
        # Delete workout exercises for each day
        for day_id in day_ids:
            cursor.execute('DELETE FROM workout_exercises WHERE workout_day_id = ?', (day_id,))
        
        # Delete workout days
        cursor.execute('DELETE FROM workout_days WHERE program_id = ?', (program_id,))
        
        # Delete the program itself
        cursor.execute('DELETE FROM workout_programs WHERE id = ?', (program_id,))
        
        self.conn.commit()

    def get_workout_statistics(self):
        """Get comprehensive workout statistics for visualization."""
        cursor = self.conn.cursor()
        
        # Get basic stats
        cursor.execute('SELECT COUNT(*) FROM workout_logs')
        total_workouts = cursor.fetchone()[0]
        
        if total_workouts == 0:
            return None
            
        # Get workouts this month
        cursor.execute('''
            SELECT COUNT(*) FROM workout_logs 
            WHERE date >= date('now', 'start of month')
        ''')
        workouts_this_month = cursor.fetchone()[0]
        
        # Calculate average duration
        cursor.execute('''
            SELECT AVG(
                (strftime('%s', end_time) - strftime('%s', start_time)) / 60
            ) FROM workout_logs
        ''')
        avg_duration = round(cursor.fetchone()[0] or 0)
        
        # Calculate consistency (percentage of planned workouts completed)
        cursor.execute('''
            SELECT COUNT(DISTINCT date) * 100.0 / 
            (SELECT COUNT(DISTINCT day_number) FROM workout_days)
            FROM workout_logs
            WHERE date >= date('now', '-30 days')
        ''')
        consistency = round(cursor.fetchone()[0] or 0)
        
        # Get weekly workout frequency
        cursor.execute('''
            SELECT strftime('%W', date) as week, COUNT(*) as workouts
            FROM workout_logs
            WHERE date >= date('now', '-12 weeks')
            GROUP BY week
            ORDER BY week
        ''')
        weekly_frequency = [{'week': row[0], 'workouts': row[1]} 
                          for row in cursor.fetchall()]
        
        # Get muscle group distribution
        cursor.execute('''
            SELECT e.muscle_group, COUNT(*) as count
            FROM exercise_logs el
            JOIN exercises e ON el.exercise_id = e.id
            GROUP BY e.muscle_group
        ''')
        muscle_groups = [{'muscle_group': row[0], 'count': row[1]} 
                        for row in cursor.fetchall()]
        
        # Get exercise type distribution
        cursor.execute('''
            SELECT e.equipment as type, COUNT(*) as count
            FROM exercise_logs el
            JOIN exercises e ON el.exercise_id = e.id
            GROUP BY e.equipment
        ''')
        exercise_types = [{'type': row[0], 'count': row[1]} 
                         for row in cursor.fetchall()]
        
        # Get list of exercises for progress tracking
        cursor.execute('''
            SELECT DISTINCT e.name
            FROM exercise_logs el
            JOIN exercises e ON el.exercise_id = e.id
            ORDER BY e.name
        ''')
        available_exercises = [row[0] for row in cursor.fetchall()]
        
        return {
            'total_workouts': total_workouts,
            'workouts_this_month': workouts_this_month,
            'avg_duration': avg_duration,
            'consistency': consistency,
            'weekly_frequency': weekly_frequency,
            'muscle_groups': muscle_groups,
            'exercise_types': exercise_types,
            'available_exercises': available_exercises
        }

    def get_exercise_progress(self, exercise_name):
        """Get progress data for a specific exercise."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                wl.date,
                MAX(el.weight) as weight,
                MAX(el.reps) as reps
            FROM exercise_logs el
            JOIN workout_logs wl ON el.workout_log_id = wl.id
            JOIN exercises e ON el.exercise_id = e.id
            WHERE e.name = ?
            GROUP BY wl.date
            ORDER BY wl.date
        ''', (exercise_name,))
        
        results = cursor.fetchall()
        if not results:
            return None
            
        return [{
            'date': row[0],
            'weight': row[1],
            'reps': row[2]
        } for row in results]

    def __del__(self):
        self.conn.close() 