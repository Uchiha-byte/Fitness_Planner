"""
Nutrition Tracker Module
Handles nutrition tracking and meal planning functionality
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from utils import FoodDatabase
from utils.db_manager import DatabaseManager

def format_food_info(food):
    """Format food information for display"""
    return f"""
• Serving Size: {food['Measure']}
• Calories: {food['Calories']:.1f}
• Protein: {food['Protein']:.1f}g
• Carbs: {food['Carbs']:.1f}g
• Fat: {food['Fat']:.1f}g
• Fiber: {food['Fiber']:.1f}g
    """

def app():
    st.title("Nutrition Tracker")
    
    # Initialize session states
    if 'food_db' not in st.session_state:
        st.session_state.food_db = FoodDatabase()
    
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    
    # Load daily goals from database
    if 'daily_goals' not in st.session_state:
        stored_goals = st.session_state.db_manager.get_daily_goals()
        if stored_goals:
            st.session_state.daily_goals = stored_goals
        else:
            st.session_state.daily_goals = {
                'calories': 2000,
                'protein': 150,
                'carbs': 250,
                'fat': 65
            }
            st.session_state.db_manager.save_daily_goals(st.session_state.daily_goals)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Add Food", "Daily Summary", "Browse Foods", "Goals"])
    
    # Tab 1: Add Food
    with tab1:
        st.header("Log Your Food")
        
        # Search box
        search_col, category_col = st.columns([2, 1])
        
        with search_col:
            search_query = st.text_input("Search for a food", key="food_search")
            if search_query:
                search_results = st.session_state.food_db.search_food(search_query)
                if search_results:
                    st.subheader("Search Results")
                    for idx, food in enumerate(search_results):
                        with st.expander(f"{food['Food']}"):
                            st.markdown(format_food_info(food))
                            
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                serving_size = st.number_input(
                                    "Serving size (grams)",
                                    min_value=1,
                                    value=int(food['Grams']),
                                    key=f"serving_{idx}_{food['Food']}"
                                )
                            
                            with col2:
                                meal_type = st.selectbox(
                                    "Meal",
                                    ["Breakfast", "Lunch", "Dinner", "Snack"],
                                    key=f"meal_{idx}_{food['Food']}"
                                )
                            
                            if st.button("Add to Log", key=f"add_{idx}_{food['Food']}"):
                                # Calculate nutrition for selected serving size
                                adjusted_nutrition = st.session_state.food_db.calculate_serving(
                                    food_id=search_results.index(food),
                                    desired_grams=serving_size
                                )
                                
                                # Add to log
                                log_entry = {
                                    'time': datetime.now().strftime("%H:%M"),
                                    'date': datetime.now().date().isoformat(),
                                    'food_name': food['Food'],
                                    'meal_type': meal_type,
                                    'serving_size': serving_size,
                                    'calories': adjusted_nutrition['Calories'],
                                    'protein': adjusted_nutrition['Protein'],
                                    'carbs': adjusted_nutrition['Carbs'],
                                    'fat': adjusted_nutrition['Fat'],
                                    'fiber': adjusted_nutrition['Fiber']
                                }
                                st.session_state.db_manager.add_food_log(log_entry)
                                st.success(f"Added {food['Food']} to your log!")
                                st.rerun()
                else:
                    st.info("No matching foods found")
        
        with category_col:
            selected_category = st.selectbox(
                "Or browse by category",
                ["All Categories"] + st.session_state.food_db.get_categories()
            )
    
    # Tab 2: Daily Summary
    with tab2:
        st.header("Daily Summary")
        
        # Add Reset Button with confirmation
        col_title, col_reset = st.columns([4, 1])
        with col_title:
            pass  # Empty column for spacing
        with col_reset:
            if st.button("Reset Today", key="reset_today", type="secondary"):
                if "confirm_reset" not in st.session_state:
                    st.session_state.confirm_reset = False
                st.session_state.confirm_reset = True
        
        if st.session_state.get("confirm_reset", False):
            st.warning("Are you sure you want to reset today's log? This cannot be undone.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Reset", key="confirm_reset_yes", type="primary"):
                    # Clear today's logs from database
                    st.session_state.db_manager.clear_logs_by_date(datetime.now().date().isoformat())
                    st.session_state.confirm_reset = False
                    st.success("Today's log has been reset!")
                    st.rerun()
            with col2:
                if st.button("Cancel", key="confirm_reset_no"):
                    st.session_state.confirm_reset = False
                    st.rerun()
        
        # Get today's logs from database
        today_logs = st.session_state.db_manager.get_logs_by_date(datetime.now().date().isoformat())
        
        if today_logs:
            # Calculate totals
            totals = {
                'calories': sum(log['calories'] for log in today_logs),
                'protein': sum(log['protein'] for log in today_logs),
                'carbs': sum(log['carbs'] for log in today_logs),
                'fat': sum(log['fat'] for log in today_logs)
            }
            
            # Display progress towards goals
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Calories",
                    f"{totals['calories']:.0f}",
                    f"{st.session_state.daily_goals['calories'] - totals['calories']:.0f} remaining"
                )
                st.progress(min(totals['calories'] / st.session_state.daily_goals['calories'], 1.0))
            
            with col2:
                st.metric(
                    "Protein",
                    f"{totals['protein']:.1f}g",
                    f"{st.session_state.daily_goals['protein'] - totals['protein']:.1f}g remaining"
                )
                st.progress(min(totals['protein'] / st.session_state.daily_goals['protein'], 1.0))
            
            with col3:
                st.metric(
                    "Carbs",
                    f"{totals['carbs']:.1f}g",
                    f"{st.session_state.daily_goals['carbs'] - totals['carbs']:.1f}g remaining"
                )
                st.progress(min(totals['carbs'] / st.session_state.daily_goals['carbs'], 1.0))
            
            with col4:
                st.metric(
                    "Fat",
                    f"{totals['fat']:.1f}g",
                    f"{st.session_state.daily_goals['fat'] - totals['fat']:.1f}g remaining"
                )
                st.progress(min(totals['fat'] / st.session_state.daily_goals['fat'], 1.0))
            
            # Macro-nutrient distribution pie chart
            st.subheader("Macro-nutrient Distribution")
            fig = px.pie(
                values=[totals['protein'], totals['carbs'], totals['fat']],
                names=['Protein', 'Carbs', 'Fat'],
                title='Macro-nutrient Distribution'
            )
            st.plotly_chart(fig)
            
            # Meal breakdown
            st.subheader("Meals")
            for meal in ["Breakfast", "Lunch", "Dinner", "Snack"]:
                with st.expander(meal):
                    meal_logs = [log for log in today_logs if log['meal_type'] == meal]
                    if meal_logs:
                        df = pd.DataFrame(meal_logs)
                        st.dataframe(
                            df[['food_name', 'serving_size', 'calories', 'protein', 'carbs', 'fat']],
                            hide_index=True
                        )
                        st.metric(f"Total {meal} Calories", f"{sum(log['calories'] for log in meal_logs):.0f}")
                    else:
                        st.info(f"No {meal.lower()} logged yet")
        else:
            st.info("No foods logged today")
    
    # Tab 3: Browse Foods
    with tab3:
        st.header("Browse Foods")
        
        # Category selection
        category = st.selectbox(
            "Select Category",
            st.session_state.food_db.get_categories()
        )
        
        # Nutrient filter
        col1, col2 = st.columns(2)
        with col1:
            nutrient = st.selectbox(
                "Sort by Nutrient",
                ["Calories", "Protein", "Carbs", "Fat", "Fiber"]
            )
        
        with col2:
            limit = st.slider("Number of items", 0, 20, 10)
        
        # Get foods for selected category
        category_foods = st.session_state.food_db.get_foods_by_category(category)
        
        # Convert to DataFrame for sorting
        if category_foods:
            df = pd.DataFrame(category_foods)
            # Sort by selected nutrient
            df = df.sort_values(by=nutrient, ascending=False).head(limit)
            # Convert back to list of dictionaries
            foods = df.to_dict('records')
            
            # Display foods
            for idx, food in enumerate(foods):
                with st.expander(f"{food['Food']} - {food[nutrient]:.1f}{' kcal' if nutrient == 'Calories' else 'g'}"):
                    st.markdown(format_food_info(food))
                    
                    # Add serving size selection
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        serving_size = st.number_input(
                            "Serving size (grams)",
                            min_value=1,
                            value=int(food['Grams']),
                            key=f"browse_serving_{idx}_{food['Food']}"
                        )
                    
                    with col2:
                        meal_type = st.selectbox(
                            "Meal",
                            ["Breakfast", "Lunch", "Dinner", "Snack"],
                            key=f"browse_meal_{idx}_{food['Food']}"
                        )
                    
                    if st.button("Add to Log", key=f"browse_{idx}_{food['Food']}"):
                        # Calculate adjusted nutrition based on serving size
                        multiplier = serving_size / food['Grams']
                        log_entry = {
                            'time': datetime.now().strftime("%H:%M"),
                            'date': datetime.now().date().isoformat(),
                            'food_name': food['Food'],
                            'meal_type': meal_type,
                            'serving_size': serving_size,
                            'calories': food['Calories'] * multiplier,
                            'protein': food['Protein'] * multiplier,
                            'carbs': food['Carbs'] * multiplier,
                            'fat': food['Fat'] * multiplier,
                            'fiber': food['Fiber'] * multiplier
                        }
                        st.session_state.db_manager.add_food_log(log_entry)
                        st.success(f"Added {food['Food']} to your log!")
                        st.rerun()
        else:
            st.info(f"No foods found in category: {category}")
    
    # Tab 4: Goals
    with tab4:
        st.header("Set Daily Goals")
        
        # Get current goals from session state
        current_goals = st.session_state.daily_goals.copy()
        
        # Create form for goals
        with st.form(key="goals_form"):
            new_goals = {}
            
            new_goals['calories'] = st.number_input(
                "Daily Calorie Goal",
                min_value=1200.0,
                max_value=5000.0,
                value=float(current_goals['calories']),
                step=50.0
            )
            
            new_goals['protein'] = st.number_input(
                "Daily Protein Goal (g)",
                min_value=30.0,
                max_value=300.0,
                value=float(current_goals['protein']),
                step=5.0
            )
            
            new_goals['carbs'] = st.number_input(
                "Daily Carbs Goal (g)",
                min_value=50.0,
                max_value=500.0,
                value=float(current_goals['carbs']),
                step=5.0
            )
            
            new_goals['fat'] = st.number_input(
                "Daily Fat Goal (g)",
                min_value=20.0,
                max_value=200.0,
                value=float(current_goals['fat']),
                step=5.0
            )
            
            # Add Set Goals button
            submitted = st.form_submit_button("Set Goals", type="primary")
            if submitted:
                if new_goals != current_goals:
                    st.session_state.daily_goals = new_goals
                    st.session_state.db_manager.save_daily_goals(new_goals)
                    st.success("Goals updated successfully!")
                    st.rerun()
                else:
                    st.info("No changes made to goals.")
        
        # Display current goals
        st.subheader("Current Goals")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Calories", f"{current_goals['calories']:.0f} kcal")
        with col2:
            st.metric("Protein", f"{current_goals['protein']:.1f}g")
        with col3:
            st.metric("Carbs", f"{current_goals['carbs']:.1f}g")
        with col4:
            st.metric("Fat", f"{current_goals['fat']:.1f}g")

if __name__ == "__main__":
    app() 