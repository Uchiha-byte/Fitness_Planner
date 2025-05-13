# ZFIT AI-Powered Fitness Tracker and Planner

ZFIT is a comprehensive fitness application that combines the power of AI with traditional fitness tracking and planning features to provide a personalized fitness experience.

## Project Structure

The application follows a modular structure with separate pages for each major feature:

```
zfit/
├── app.py
├── pages/
│   ├── exercise_library.py
│   ├── nutrition_tracker.py
│   ├── workout_planner.py
│   ├── ai_coach.py
│   └── food_vision.py
├── requirements.txt
└── README.md
```

## Features

1. **Exercise Library** (Implemented)
   - Comprehensive collection of exercises for each body part
   - Detailed instructions and form guidance
   - Sets, reps, and rest recommendations

2. **Nutrition Tracker** (In Development)
   - Track daily calorie intake
   - Monitor macronutrients (protein, carbs, fats)
   - Visual progress charts and analytics
   - Customizable goals and targets

3. **Workout Planner** (In Development)
   - Create custom workout plans
   - Choose from pre-made templates
   - Flexible scheduling options
   - Progress tracking

4. **AI Coach** (In Development)
   - Get personalized fitness advice
   - Form check recommendations
   - Nutrition guidance
   - Progress-based suggestions

5. **Food Vision** (In Development)
   - Upload food pictures for nutrition estimation
   - AI-powered food recognition using OpenCV
   - Automatic nutrition facts calculation
   - Quick and easy logging

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/uchiha_byte/Fitness_Planner.git
cd zfit
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add:
```
OPENAI_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Getting Started**
   - Launch the application using `streamlit run app.py`
   - Navigate through different sections using the sidebar navigation
   - Set up your profile and fitness goals

2. **Exercise Library**
   - Browse exercises by category
   - View detailed exercise instructions
   - Get recommended sets, reps, and rest periods

3. **Additional Features**
   - More features are currently under development
   - Check back for updates on nutrition tracking, workout planning, AI coaching, and food vision features

## Technologies Used

- Python
- Streamlit
- OpenCV (for computer vision tasks)
- OpenAI API
- Pandas
- Plotly
- PIL (Python Imaging Library)

## Development Status

The application is currently undergoing modularization. The following modules have been implemented:
- Home page
- Exercise Library

The following modules are under development:
- Nutrition Tracker
- Workout Planner
- AI Coach
- Food Vision

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. #
