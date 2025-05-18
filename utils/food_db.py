import pandas as pd
import numpy as np
from pathlib import Path

class FoodDatabase:
    def __init__(self):
        self.db_path = Path('data/food_database.csv')
        self.foods_df = None
        self.load_database()
        
    def load_database(self):
        """Load and preprocess the food database"""
        try:
            self.foods_df = pd.read_csv(self.db_path)
            # Clean up column names
            self.foods_df.columns = [col.strip() for col in self.foods_df.columns]
            
            # Replace 't' (trace) values with 0.1 and convert numeric columns
            numeric_columns = ['Calories', 'Protein', 'Fat', 'Sat.Fat', 'Fiber', 'Carbs', 'Grams']
            for col in numeric_columns:
                # Replace 't' with 0.1 if present
                if col in self.foods_df.columns:
                    self.foods_df[col] = self.foods_df[col].replace('t', '0.1')
                    # Convert to numeric, replacing errors with 0
                    self.foods_df[col] = pd.to_numeric(self.foods_df[col], errors='coerce').fillna(0)
            
        except Exception as e:
            print(f"Error loading food database: {e}")
            self.foods_df = pd.DataFrame()
    
    def search_food(self, query, limit=10):
        """Search for foods by name"""
        if self.foods_df is None or self.foods_df.empty:
            return []
        
        # Convert query to lowercase for case-insensitive search
        query = query.lower()
        mask = self.foods_df['Food'].str.lower().str.contains(query, na=False)
        matches = self.foods_df[mask].head(limit)
        
        # Convert to list of dictionaries
        return matches.to_dict('records')
    
    def get_categories(self):
        """Get list of all unique food categories"""
        if self.foods_df is None or self.foods_df.empty:
            return []
        return sorted(self.foods_df['Category'].unique().tolist())
    
    def get_foods_by_category(self, category):
        """Get all foods in a specific category"""
        if self.foods_df is None or self.foods_df.empty:
            return []
        
        category_foods = self.foods_df[self.foods_df['Category'] == category]
        return category_foods.to_dict('records')
    
    def get_foods_by_nutrient(self, nutrient, min_value=None, max_value=None, limit=10):
        """Get foods filtered by nutrient value"""
        if self.foods_df is None or self.foods_df.empty:
            return []
        
        df = self.foods_df.copy()
        
        if min_value is not None:
            df = df[df[nutrient] >= min_value]
        if max_value is not None:
            df = df[df[nutrient] <= max_value]
            
        return df.nlargest(limit, nutrient).to_dict('records')
    
    def calculate_serving(self, food_id, desired_grams):
        """Calculate nutritional values for a custom serving size"""
        if self.foods_df is None or self.foods_df.empty:
            return None
            
        food = self.foods_df.iloc[food_id]
        if food is None:
            return None
            
        # Calculate multiplier based on desired grams
        multiplier = desired_grams / food['Grams']
        
        return {
            'Food': food['Food'],
            'Measure': f"{desired_grams}g",
            'Calories': food['Calories'] * multiplier,
            'Protein': food['Protein'] * multiplier,
            'Fat': food['Fat'] * multiplier,
            'Sat.Fat': food['Sat.Fat'] * multiplier,
            'Fiber': food['Fiber'] * multiplier,
            'Carbs': food['Carbs'] * multiplier
        } 