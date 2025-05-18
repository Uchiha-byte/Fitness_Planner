# -*- coding: utf-8 -*-
"""
Workout Planner Module
Handles workout planning and tracking functionality
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils.workout_db import WorkoutDatabase
from utils.ai_trainer import AITrainer
import json
import os

def format_exercise_info(exercise):
    """Format exercise information for display"""
    return f"""
• Name: {exercise['name']}
• Muscle Group: {exercise['muscle_group']}
• Equipment: {exercise['equipment']}
• Difficulty: {exercise['difficulty']}
    """

def app():
    st.title("Smart Workout Planner")
    
    # Initialize database and AI trainer
    if 'workout_db' not in st.session_state:
        st.session_state.workout_db = WorkoutDatabase()
    
    if 'ai_trainer' not in st.session_state:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            st.error("Please set the GEMINI_API_KEY environment variable to use AI features.")
            return
        st.session_state.ai_trainer = AITrainer(api_key)
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs([
        "Smart Program Creator", "Workout Log", "Progress Tracking"
    ])
    
    # Tab 1: Smart Program Creator
    with tab1:
        st.header("Create Your Perfect Workout Program")
        
        with st.form("smart_program_form"):
            goal = st.selectbox(
                "What's your main goal?",
                ["Build Muscle", "Lose Fat", "Gain Strength", "General Fitness", "Athletic Performance", 
                 "Endurance", "Flexibility", "Power", "Sport Specific"]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                fitness_level = st.selectbox(
                    "Experience Level",
                    ["Beginner", "Intermediate", "Advanced"]
                )
                days_per_week = st.selectbox(
                    "Days per week",
                    [2, 3, 4, 5, 6],
                    index=1
                )
            
            with col2:
                time_per_session = st.selectbox(
                    "Minutes per workout",
                    [30, 45, 60, 75, 90],
                    index=1
                )
                duration_weeks = st.selectbox(
                    "Program duration (weeks)",
                    [4, 6, 8, 10, 12],
                    index=0
                )
            
            equipment = st.multiselect(
                "Available Equipment",
                ["Bodyweight", "Dumbbells", "Barbell", "Cables", "Machines", 
                 "Resistance Bands", "Kettlebells", "Pull-up Bar", "Suspension Trainer (TRX)", 
                 "Medicine Ball", "Foam Roller", "Yoga Mat", "Bench", "Smith Machine",
                 "Power Rack", "Olympic Rings", "Plates", "Box/Platform", "Battle Ropes"],
                default=["Bodyweight", "Dumbbells"]
            )
            
            if st.form_submit_button("Generate Program"):
                with st.spinner("Creating your personalized workout program..."):
                    user_input = {
                        'goal': goal,
                        'fitness_level': fitness_level,
                        'days_per_week': days_per_week,
                        'time_per_session': time_per_session,
                        'duration_weeks': duration_weeks,
                        'equipment': equipment
                    }
                    
                    program = st.session_state.ai_trainer.generate_workout_program(user_input)
                    
                    if program:
                        program_id = st.session_state.workout_db.create_workout_program({
                            'name': program['name'],
                            'description': program['description'],
                            'frequency': program['frequency'],
                            'duration_weeks': program['duration_weeks'],
                            'difficulty': program['difficulty'],
                            'tags': program['tags']
                        })
                        
                        for day in program['workout_days']:
                            day_id = st.session_state.workout_db.add_workout_day(program_id, {
                                'day_number': day['day_number'],
                                'name': day['name']
                            })
                            
                            for ex in day['exercises']:
                                exercise_data = {
                                    'name': ex['name'],
                                    'description': '',
                                    'muscle_group': 'Unknown',
                                    'equipment': 'Unknown',
                                    'difficulty': program['difficulty'],
                                    'instructions': ex.get('notes', ''),
                                    'is_custom': False
                                }
                                ex_id = st.session_state.workout_db.add_exercise(exercise_data)
                                
                                st.session_state.workout_db.add_workout_exercise(day_id, {
                                    'exercise_id': ex_id,
                                    'sets': ex['sets'],
                                    'reps': ex['reps'],
                                    'rest_seconds': ex.get('rest_seconds', 60),
                                    'notes': ex.get('notes', ''),
                                    'order_in_workout': ex['order']
                                })
                        
                        st.success("Your personalized workout program has been created!")
                        st.session_state.current_program = program_id
                        st.rerun()
        
        # Display existing programs
        st.subheader("Your Programs")
        programs = st.session_state.workout_db.get_workout_programs()
        if programs:
            for program in programs:
                with st.expander(f"{program['name']} - {program['difficulty']}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(program['description'])
                        st.write(f"Frequency: {program['frequency']}")
                        st.write(f"Duration: {program['duration_weeks']} weeks")
                    with col2:
                        if st.button("Delete Program", key=f"delete_{program['id']}"):
                            st.session_state.workout_db.delete_program(program['id'])
                            st.success(f"Program '{program['name']}' deleted successfully!")
                            st.rerun()
                    
                    days = st.session_state.workout_db.get_workout_days(program['id'])
                    if days:
                        for day in days:
                            st.subheader(f"Day {day['day_number']}: {day['name']}")
                            exercises = st.session_state.workout_db.get_workout_exercises(day['id'])
                            if exercises:
                                for ex in exercises:
                                    with st.container():
                                        st.markdown(f"**{ex['name']} - {ex['sets']} sets**")
                                        st.write(f"Reps: {json.loads(ex['reps'])}")
                                        st.write(f"Rest: {ex['rest_seconds']} seconds")
                                        if ex['notes']:
                                            st.write(f"Notes: {ex['notes']}")
                                        
                                        if st.button("Show Form Tips", key=f"tips_{ex['id']}"):
                                            with st.spinner("Getting expert form tips..."):
                                                tips = st.session_state.ai_trainer.generate_form_tips(ex['name'])
                                                if tips:
                                                    with st.container():
                                                        col1, col2 = st.columns(2)
                                                        with col1:
                                                            st.markdown("**Quick Setup**")
                                                            st.write(tips['setup'][0])
                                                            st.markdown("**Key Form Points**")
                                                            st.write("• " + tips['execution'][0])
                                                        with col2:
                                                            st.markdown("**Watch Out For**")
                                                            st.write("• " + tips['common_mistakes'][0])
                                                            st.markdown("**Safety First**")
                                                            st.write("• " + tips['safety_tips'][0])
                                                        st.markdown("**Quick Tips**")
                                                        st.write(f"Breathing: {tips['breathing']} | Variation: {tips['variations'][0]}")
                                        st.divider()
                    
                    with st.form(f"feedback_{program['id']}"):
                        feedback = st.text_area("How is this program working for you? Share your experience and challenges:")
                        if st.form_submit_button("Get Personalized Modifications"):
                            with st.spinner("Analyzing your feedback..."):
                                modifications = st.session_state.ai_trainer.suggest_workout_modifications(
                                    {'program': program, 'days': days},
                                    feedback
                                )
                                if modifications:
                                    st.subheader("Suggested Modifications")
                                    for mod in modifications['modifications']:
                                        st.write(f"**{mod['exercise']}**")
                                        st.write(f"Change: {mod['change']}")
                                        st.write(f"Reason: {mod['reason']}")
                                        st.write(f"Alternative: {mod['alternative']}")
                                    st.subheader("General Advice")
                                    st.write(modifications['general_advice'])
    
    # Tab 2: Workout Log
    with tab2:
        st.header("Workout Log")
        
        # Start new workout section
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_program = st.selectbox(
                "Select Program",
                [p['name'] for p in programs] if programs else ["No programs available"]
            )
        with col2:
            if st.button("Start Workout", disabled=not programs):
                st.session_state.active_workout = {
                    'start_time': datetime.now(),
                    'exercises': []
                }
                st.rerun()
        
        # Active workout section
        if hasattr(st.session_state, 'active_workout'):
            st.subheader("Current Workout")
            duration = datetime.now() - st.session_state.active_workout['start_time']
            st.write(f"Duration: {str(duration).split('.')[0]}")
            
            # Exercise logging
            with st.form("exercise_log_form"):
                exercise = st.selectbox("Exercise", [ex['name'] for ex in exercises])
                col1, col2, col3 = st.columns(3)
                with col1:
                    weight = st.number_input("Weight (kg)", min_value=0.0, step=2.5)
                with col2:
                    reps = st.number_input("Reps", min_value=1)
                with col3:
                    rpe = st.slider("RPE", 1, 10, 7)
                
                notes = st.text_input("Notes (optional)")
                
                if st.form_submit_button("Log Set"):
                    # Find exercise ID
                    ex_id = next(ex['id'] for ex in exercises if ex['name'] == exercise)
                    set_data = {
                        'exercise_id': ex_id,
                        'weight': weight,
                        'reps': reps,
                        'rpe': rpe,
                        'notes': notes
                    }
                    st.session_state.active_workout['exercises'].append(set_data)
                    st.success("Set logged successfully!")
                    st.rerun()
            
            # Display logged sets
            if st.session_state.active_workout['exercises']:
                st.subheader("Logged Sets")
                for idx, set_data in enumerate(st.session_state.active_workout['exercises'], 1):
                    ex_name = next(ex['name'] for ex in exercises if ex['id'] == set_data['exercise_id'])
                    st.write(f"{idx}. {ex_name}: {set_data['weight']}kg × {set_data['reps']} reps @ RPE {set_data['rpe']}")
            
            # Finish workout button
            if st.button("Finish Workout"):
                workout_data = {
                    'date': datetime.now().date().isoformat(),
                    'start_time': st.session_state.active_workout['start_time'].strftime("%H:%M"),
                    'end_time': datetime.now().strftime("%H:%M"),
                    'notes': '',
                    'rating': None
                }
                workout_log_id = st.session_state.workout_db.log_workout(workout_data)
                
                # Log all sets
                for idx, set_data in enumerate(st.session_state.active_workout['exercises'], 1):
                    log_data = {
                        'workout_log_id': workout_log_id,
                        'exercise_id': set_data['exercise_id'],
                        'set_number': idx,
                        'reps': set_data['reps'],
                        'weight': set_data['weight'],
                        'rpe': set_data['rpe'],
                        'notes': set_data.get('notes', '')
                    }
                    st.session_state.workout_db.log_exercise_set(log_data)
                
                del st.session_state.active_workout
                st.success("Workout completed and logged successfully!")
                st.rerun()
    
    # Tab 3: Progress Tracking
    with tab3:
        st.header("Progress Tracking")
        
        # Get workout statistics
        workout_stats = st.session_state.workout_db.get_workout_statistics()
        
        if workout_stats:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Workouts", workout_stats['total_workouts'])
            with col2:
                st.metric("This Month", workout_stats['workouts_this_month'])
            with col3:
                st.metric("Avg. Duration", f"{workout_stats['avg_duration']} min")
            with col4:
                st.metric("Consistency", f"{workout_stats['consistency']}%")

            # Workout frequency over time
            st.subheader("Workout Frequency")
            freq_df = pd.DataFrame(workout_stats['weekly_frequency'])
            if not freq_df.empty:
                fig_freq = px.line(
                    freq_df,
                    x='week',
                    y='workouts',
                    title='Workouts per Week'
                )
                fig_freq.update_layout(
                    xaxis_title="Week",
                    yaxis_title="Number of Workouts"
                )
                st.plotly_chart(fig_freq, use_container_width=True)

            # Exercise distribution
            st.subheader("Exercise Distribution")
            col1, col2 = st.columns(2)
            
            with col1:
                muscle_df = pd.DataFrame(workout_stats['muscle_groups'])
                if not muscle_df.empty:
                    fig_muscle = px.pie(
                        muscle_df,
                        values='count',
                        names='muscle_group',
                        title='Muscle Group Focus'
                    )
                    st.plotly_chart(fig_muscle)
            
            with col2:
                type_df = pd.DataFrame(workout_stats['exercise_types'])
                if not type_df.empty:
                    fig_type = px.pie(
                        type_df,
                        values='count',
                        names='type',
                        title='Exercise Types'
                    )
                    st.plotly_chart(fig_type)

            # Progress charts
            st.subheader("Strength Progress")
            if workout_stats['available_exercises']:
                exercise_choice = st.selectbox(
                    "Select Exercise",
                    workout_stats['available_exercises']
                )
                
                if exercise_choice:
                    progress_data = st.session_state.workout_db.get_exercise_progress(exercise_choice)
                    if progress_data:
                        progress_df = pd.DataFrame(progress_data)
                        fig_progress = px.line(
                            progress_df,
                            x='date',
                            y=['weight', 'reps'],
                            title=f'{exercise_choice} Progress',
                            labels={'value': 'Weight (kg) / Reps', 'variable': 'Metric'}
                        )
                        fig_progress.update_layout(
                            xaxis_title="Date",
                            yaxis_title="Value",
                            legend_title="Metric"
                        )
                        st.plotly_chart(fig_progress, use_container_width=True)
                    else:
                        st.info("No progress data available for this exercise yet.")
            else:
                st.info("Log some exercises to track your strength progress!")
        else:
            st.info("Complete some workouts to see your progress statistics!")

if __name__ == "__main__":
    app() 