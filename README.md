# ZFIT - AI-Powered Fitness Planner

ZFIT is an intelligent fitness tracking and planning application that leverages AI to provide personalized workout and nutrition guidance. The application helps users achieve their fitness goals through smart workout planning, nutrition tracking, and progress monitoring.

## 🌟 Features

### 1. Smart Workout Planning
- Personalized workout plans based on fitness goals
- Comprehensive exercise library with detailed instructions
- Video demonstrations for proper form
- Difficulty levels and target muscle groups
- Training parameters (sets, reps, rest periods)

### 2. Nutrition Tracking
- Daily nutrition goals and tracking
- Macro-nutrient monitoring
- Food logging with calorie tracking
- AI-powered nutrition recommendations
- Progress visualization

### 3. AI Coach
- 24/7 virtual fitness coaching
- Form check assistance
- Personalized workout advice
- Nutrition guidance
- Goal setting and tracking

### 4. Progress Tracking
- Weight and body composition tracking
- Workout performance metrics
- Visual progress charts
- Goal achievement tracking
- Weekly and monthly summaries

### 5. Food Vision
- AI-powered food recognition
- Instant nutritional information
- Calorie and macro tracking
- Meal logging made easy

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/uchiha_byte/Ai_FitnessPlanner.git
cd Ai_FitnessPlanner
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add:
```
GEMINI_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run app.py
```

## 📁 Project Structure

```
Ai_FitnessPlanner/
├── app.py                 # Main application file
├── config.py             # Configuration and constants
├── requirements.txt      # Python dependencies
├── static/              # Static assets
│   └── css/
│       └── style.css    # Custom styling
├── pages/               # Application pages
│   ├── auth.py         # Authentication
│   ├── exercise_library.py
│   ├── workout_planner.py
│   ├── nutrition_tracker.py
│   ├── ai_coach.py
│   └── food_vision.py
├── utils/              # Utility functions
│   ├── db_manager.py   # Database operations
│   └── state_management.py
└── data/              # Data storage
    └── fitness_data.db
```

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **AI/ML**: Google Gemini API
- **Version Control**: Git

## 🔧 Configuration

The application uses several configuration files:

1. `config.py`: Contains application constants and exercise data
2. `.env`: Stores sensitive information like API keys
3. `requirements.txt`: Lists all Python dependencies

## 📊 Database Schema

The application uses SQLite with the following main tables:
- Users
- Workout Logs
- Nutrition Logs
- Progress Tracking
- Daily Goals

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- Streamlit for the web framework
- All contributors and users of the application

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

## 🔄 Updates

### Version 2.0
- Added AI Coach feature
- Implemented Food Vision
- Enhanced progress tracking
- Improved UI/UX
- Added dark theme support

### Version 1.0
- Initial release
- Basic workout planning
- Nutrition tracking
- Progress monitoring
