import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = "AIzaSyBLGT29OGmcA4dPxJAmHbbYPkZUScpWOI0"
GEMINI_API_KEY = "AIzaSyBLGT29OGmcA4dPxJAmHbbYPkZUScpWOI0"

# Model Names
GEMINI_MODEL = "gemini-pro"
GEMINI_VISION_MODEL = "gemini-pro-vision"

# Model configuration
EXERCISE_DATA = {
    "Chest": {
        "Push-Ups": {
            "description": "A fundamental bodyweight exercise that primarily targets the chest muscles while engaging the shoulders and triceps.",
            "difficulty": "Beginner",
            "target_muscles": ["Chest", "Shoulders", "Triceps"],
            "video_url": "https://www.youtube.com/watch?v=IODxDxX7oi4",
            "instructions": [
                "Start in a plank position with hands slightly wider than shoulders",
                "Keep your body in a straight line from head to heels",
                "Lower your chest to the ground by bending your elbows",
                "Push back up to the starting position",
                "Keep your core tight throughout the movement"
            ],
            "sets": "3",
            "reps": "10-15",
            "rest": "60 sec",
            "tips": [
                "Keep your elbows at a 45-degree angle",
                "Look at a spot on the ground about 6 inches in front of you",
                "Breathe steadily throughout the movement"
            ],
            "common_mistakes": [
                "Sagging hips",
                "Flaring elbows too wide",
                "Not going low enough"
            ]
        },
        "Bench Press": {
            "description": "A compound exercise that builds chest strength and muscle mass using a barbell or dumbbells.",
            "difficulty": "Intermediate",
            "target_muscles": ["Chest", "Shoulders", "Triceps"],
            "video_url": "https://www.youtube.com/watch?v=hWbUlkb5Ms4",
            "instructions": [
                "Lie on a flat bench with feet firmly planted on the ground",
                "Grip the bar slightly wider than shoulder width",
                "Unrack the bar and lower it to your chest with control",
                "Press the bar back up to starting position",
                "Keep your wrists straight and elbows tucked"
            ],
            "sets": "4",
            "reps": "8-12",
            "rest": "90 sec",
            "tips": [
                "Keep your back flat on the bench",
                "Drive through your feet for stability",
                "Control the weight throughout the movement"
            ],
            "common_mistakes": [
                "Bouncing the bar off chest",
                "Arching back excessively",
                "Uneven bar path"
            ]
        }
    },
    "Back": {
        "Pull-Ups": {
            "description": "A challenging bodyweight exercise that builds upper body strength and muscle definition.",
            "difficulty": "Intermediate",
            "target_muscles": ["Lats", "Biceps", "Upper Back"],
            "video_url": "https://www.youtube.com/watch?v=eGo4IYlbE5g",
            "instructions": [
                "Hang from a pull-up bar with hands slightly wider than shoulders",
                "Pull yourself up until your chin is over the bar",
                "Lower yourself back down with control",
                "Keep your core engaged throughout"
            ],
            "sets": "3",
            "reps": "6-10",
            "rest": "90 sec",
            "tips": [
                "Start from a dead hang",
                "Focus on squeezing your shoulder blades",
                "Use a controlled tempo"
            ],
            "common_mistakes": [
                "Swinging body",
                "Not completing full range of motion",
                "Using momentum instead of control"
            ]
        },
        "Bent-Over Rows": {
            "description": "An exercise that targets the middle back muscles and helps improve posture.",
            "instructions": [
                "Bend at hips and knees, keeping back straight",
                "Hold weight with arms extended",
                "Pull weight to lower chest",
                "Lower weight back down with control"
            ],
            "sets": "3-4",
            "reps": "8-12",
            "rest": "60-90 seconds"
        }
    },
    "Legs": {
        "Squats": {
            "description": "A fundamental lower body exercise that builds strength and muscle in the legs and core.",
            "difficulty": "Beginner",
            "target_muscles": ["Quadriceps", "Hamstrings", "Glutes", "Core"],
            "video_url": "https://www.youtube.com/watch?v=U3HlEF_E9fo",
            "instructions": [
                "Stand with feet shoulder-width apart",
                "Keep chest up and core tight",
                "Lower your body by bending knees and hips",
                "Keep knees in line with toes",
                "Return to starting position"
            ],
            "sets": "4",
            "reps": "10-15",
            "rest": "90 sec",
            "tips": [
                "Keep your weight in your heels",
                "Break at your hips first",
                "Keep your back straight"
            ],
            "common_mistakes": [
                "Knees caving inward",
                "Rounding the back",
                "Not going deep enough"
            ]
        }
    },
    "Shoulders": {
        "Military Press": {
            "description": "A compound exercise that targets the deltoids and builds overall shoulder strength.",
            "difficulty": "Intermediate",
            "target_muscles": ["Deltoids", "Trapezius", "Triceps"],
            "video_url": "https://www.youtube.com/watch?v=2yjwXTZQDDI",
            "instructions": [
                "Stand with feet shoulder-width apart",
                "Hold barbell at shoulder level with palms facing forward",
                "Press the weight overhead until arms are fully extended",
                "Lower the weight back to shoulder level with control",
                "Keep core engaged throughout the movement"
            ],
            "sets": "4",
            "reps": "8-12",
            "rest": "90 sec",
            "tips": [
                "Keep your wrists straight",
                "Engage your core throughout",
                "Avoid leaning back excessively"
            ],
            "common_mistakes": [
                "Arching the back",
                "Using momentum",
                "Not fully extending arms"
            ]
        },
        "Lateral Raises": {
            "description": "An isolation exercise that targets the lateral deltoids for broader shoulders.",
            "difficulty": "Beginner",
            "target_muscles": ["Lateral Deltoids", "Trapezius"],
            "video_url": "https://www.youtube.com/watch?v=3VcKaXpzqRo",
            "instructions": [
                "Stand with dumbbells at your sides",
                "Keep a slight bend in your elbows",
                "Raise arms out to the sides until parallel with ground",
                "Lower weights back down with control",
                "Maintain proper posture throughout"
            ],
            "sets": "3",
            "reps": "12-15",
            "rest": "60 sec",
            "tips": [
                "Lead with your elbows",
                "Keep shoulders down",
                "Control the descent"
            ],
            "common_mistakes": [
                "Using too much weight",
                "Swinging the weights",
                "Raising above shoulder level"
            ]
        }
    },
    "Arms": {
        "Bicep Curls": {
            "description": "A classic isolation exercise for building bicep strength and size.",
            "difficulty": "Beginner",
            "target_muscles": ["Biceps", "Forearms"],
            "video_url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
            "instructions": [
                "Stand with dumbbells at your sides",
                "Keep elbows close to your body",
                "Curl weights up toward shoulders",
                "Lower weights back down with control",
                "Maintain straight wrists throughout"
            ],
            "sets": "3",
            "reps": "12-15",
            "rest": "60 sec",
            "tips": [
                "Keep your back straight",
                "Focus on squeezing biceps",
                "Use full range of motion"
            ],
            "common_mistakes": [
                "Swinging the body",
                "Using too much weight",
                "Not controlling the descent"
            ]
        },
        "Tricep Pushdowns": {
            "description": "An effective isolation exercise for developing tricep strength and definition.",
            "difficulty": "Beginner",
            "target_muscles": ["Triceps"],
            "video_url": "https://www.youtube.com/watch?v=2-LAMcpzODU",
            "instructions": [
                "Stand facing cable machine with high attachment",
                "Grab rope or bar at chest level",
                "Keep elbows at sides and push down",
                "Extend arms fully and squeeze triceps",
                "Return to starting position with control"
            ],
            "sets": "3",
            "reps": "12-15",
            "rest": "60 sec",
            "tips": [
                "Keep elbows tucked",
                "Focus on tricep contraction",
                "Maintain upright posture"
            ],
            "common_mistakes": [
                "Moving elbows away from body",
                "Using momentum",
                "Incomplete range of motion"
            ]
        }
    },
    "Core": {
        "Plank": {
            "description": "A fundamental isometric exercise that strengthens the entire core.",
            "difficulty": "Beginner",
            "target_muscles": ["Abs", "Lower Back", "Obliques"],
            "video_url": "https://www.youtube.com/watch?v=ASdvN_XEl_c",
            "instructions": [
                "Start in push-up position on forearms",
                "Keep body in straight line from head to heels",
                "Engage core and glutes",
                "Hold position for prescribed time",
                "Breathe steadily throughout"
            ],
            "sets": "3",
            "reps": "30-60 sec",
            "rest": "45 sec",
            "tips": [
                "Keep hips level",
                "Look at the floor",
                "Breathe consistently"
            ],
            "common_mistakes": [
                "Sagging hips",
                "Raising hips too high",
                "Holding breath"
            ]
        },
        "Russian Twists": {
            "description": "A dynamic exercise that targets the obliques and rotational core strength.",
            "difficulty": "Intermediate",
            "target_muscles": ["Obliques", "Abs", "Hip Flexors"],
            "video_url": "https://www.youtube.com/watch?v=wkD8rjkodUI",
            "instructions": [
                "Sit with knees bent and feet off ground",
                "Lean back slightly, maintaining straight back",
                "Hold weight at chest level",
                "Rotate torso side to side",
                "Touch weight to ground on each side"
            ],
            "sets": "3",
            "reps": "20 total",
            "rest": "60 sec",
            "tips": [
                "Keep chest up",
                "Control the movement",
                "Engage core throughout"
            ],
            "common_mistakes": [
                "Rounding the back",
                "Moving too quickly",
                "Not rotating fully"
            ]
        }
    },
    "Full Body": {
        "Burpees": {
            "description": "A high-intensity full body exercise that builds strength and endurance.",
            "difficulty": "Intermediate",
            "target_muscles": ["Legs", "Chest", "Core", "Shoulders"],
            "video_url": "https://www.youtube.com/watch?v=TU8QYVW0gDU",
            "instructions": [
                "Start standing, then drop into a squat",
                "Kick feet back to plank position",
                "Perform a push-up",
                "Jump feet back to squat",
                "Jump up explosively with arms overhead"
            ],
            "sets": "3",
            "reps": "10-15",
            "rest": "90 sec",
            "tips": [
                "Keep core tight throughout",
                "Land softly",
                "Pace yourself"
            ],
            "common_mistakes": [
                "Poor push-up form",
                "Not fully extending on jump",
                "Rushing the movement"
            ]
        },
        "Turkish Get-Up": {
            "description": "A complex full body exercise that improves strength, stability, and mobility.",
            "difficulty": "Advanced",
            "target_muscles": ["Shoulders", "Core", "Legs", "Hip Flexors"],
            "video_url": "https://www.youtube.com/watch?v=0bWRPC49-KI",
            "instructions": [
                "Lie on back holding weight overhead in one arm",
                "Roll to elbow while keeping arm vertical",
                "Push up to seated position",
                "Sweep back leg through to half-kneeling",
                "Stand up while maintaining weight overhead"
            ],
            "sets": "3",
            "reps": "5-8 per side",
            "rest": "90 sec",
            "tips": [
                "Keep eyes on the weight",
                "Move slowly and controlled",
                "Maintain vertical arm"
            ],
            "common_mistakes": [
                "Losing arm alignment",
                "Rushing the movement",
                "Poor weight control"
            ]
        }
    }
}

NUTRITION_GOALS = {
    "Weight Loss": {
        "calorie_deficit": 500,
        "protein_ratio": 0.4,
        "carb_ratio": 0.3,
        "fat_ratio": 0.3
    },
    "Muscle Gain": {
        "calorie_surplus": 300,
        "protein_ratio": 0.35,
        "carb_ratio": 0.45,
        "fat_ratio": 0.2
    },
    "Maintenance": {
        "calorie_adjustment": 0,
        "protein_ratio": 0.3,
        "carb_ratio": 0.4,
        "fat_ratio": 0.3
    }
}

WORKOUT_TEMPLATES = {
    "Beginner Full Body": {
        "frequency": 3,
        "exercises_per_workout": 6,
        "sets_per_exercise": "2-3",
        "rest_between_sets": "60-90 seconds"
    },
    "Intermediate Split": {
        "frequency": 4,
        "exercises_per_workout": 8,
        "sets_per_exercise": "3-4",
        "rest_between_sets": "60-120 seconds"
    },
    "Advanced PPL": {
        "frequency": 6,
        "exercises_per_workout": 6,
        "sets_per_exercise": "3-5",
        "rest_between_sets": "90-180 seconds"
    }
} 