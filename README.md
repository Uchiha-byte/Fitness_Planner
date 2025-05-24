# ZFIT - AI-Powered Fitness Tracker and Planner

<div align="center">
    <h1>🏋️‍♂️ ZFIT</h1>
    <p><em>Transform Your Life with AI-Powered Fitness</em></p>
</div>

## 🌟 Overview

ZFIT is a state-of-the-art fitness application that combines artificial intelligence with comprehensive fitness tracking and planning capabilities. Built with modern technology and designed with user experience in mind, ZFIT helps you achieve your fitness goals through personalized guidance and real-time tracking.

## 📁 Project Structure

```
ZFIT/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── requirements.txt      # Project dependencies
├── README.md            # Project documentation
├── fitness_data.db      # SQLite database
│
├── pages/               # Application pages
│   ├── __init__.py
│   ├── exercise_library.py
│   ├── workout_planner.py
│   ├── nutrition_tracker.py
│   ├── ai_coach.py
│   └── food_vision.py
│
├── static/              # Static assets
│   ├── css/
│   │   └── style.css   # Main stylesheet
│   └── images/         # Image assets
│
├── utils/              # Utility functions
│   ├── __init__.py
│   └── helpers.py
│
├── data/               # Data storage
│   ├── exercises/     # Exercise data
│   └── nutrition/     # Nutrition data
│
└── venv/               # Virtual environment (not tracked)
```

## ✨ Features

### 🎯 Core Features

- **AI-Powered Workout Planning**
  - Personalized workout recommendations
  - Dynamic adjustment based on progress
  - Form correction and technique guidance

- **Nutrition Tracking**
  - Intelligent meal planning
  - Calorie and macro tracking
  - Food vision recognition
  - Personalized dietary recommendations

- **Progress Monitoring**
  - Visual progress tracking
  - Performance analytics
  - Goal setting and achievement tracking
  - AI-driven progress insights

- **Exercise Library**
  - Comprehensive exercise database
  - HD video demonstrations
  - Detailed form instructions
  - Muscle group targeting

### 🤖 Enhanced AI Coach (Gemini API)

- **Strict, No-Nonsense Chat**
  - Direct, actionable, and concise advice
  - Responses formatted as bold bullet points, each on a new line
  - 80-120 word limit for clarity and focus
  - Strong, motivational, and evidence-based language

- **Quick Assist Buttons**
  - Instant access to expert guidance on:
    - Form Check
    - Nutrition Tips
    - Recovery Protocol
    - Motivation
    - Injury Prevention
    - Breaking Plateaus
  - Each output is organized in clear, bold points for easy reading

- **Personalized Guidance**
  - Considers your workout history and nutrition data
  - Suggests the best workout plan for your goals
  - Efficient, point-based chat for all fitness and nutrition questions

- **Modern Conversational UI**
  - Chat with your AI Coach in a natural, interactive way
  - All responses are formatted for maximum readability and actionability

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/zfit.git
cd zfit
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file and add your configurations
cp .env.example .env
```

5. Run the application:
```bash
streamlit run app.py
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: Gemini API, TensorFlow, OpenAI
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Computer Vision**: OpenCV
- **Database**: SQLite

## 📱 User Interface

- Modern, responsive design
- Intuitive navigation
- Dark mode support
- Interactive dashboards
- Real-time updates

## 🔒 Security Features

- Secure user authentication
- Data encryption
- Privacy-focused design
- Regular security updates
- GDPR compliance

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for AI capabilities
- Google Gemini API for advanced AI chat
- Streamlit for the amazing framework
- Our amazing contributors and community

## 🔄 Version History

- v2.0.0 (Current)
  - Enhanced AI Coach with Gemini API
  - Quick Assist and strict, point-based chat
  - Improved UI/UX
  - New features added
- v1.0.0
  - Initial release

---

<div align="center">
    <p>Made with ❤️ by the ZFIT Team</p>
    <p>© 2024 ZFIT. All rights reserved.</p>
</div>
