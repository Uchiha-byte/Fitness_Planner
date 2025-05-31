import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Model Names
GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_VISION_MODEL = "gemini-1.5-flash"

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
            "description": "A classic compound exercise that builds chest strength and size, also engaging shoulders and triceps.",
            "difficulty": "Intermediate",
            "target_muscles": ["Chest", "Shoulders", "Triceps"],
            "video_url": "https://www.youtube.com/watch?v=rT7DgCr-3pg",
            "instructions": [
                "Lie on bench with feet flat on the ground",
                "Grip bar slightly wider than shoulder width",
                "Lower bar to mid-chest with controlled movement",
                "Press bar back up to starting position",
                "Keep shoulders retracted throughout movement"
            ],
            "sets": "4",
            "reps": "8-12",
            "rest": "90 sec",
            "tips": [
                "Keep wrists straight and aligned with forearms",
                "Maintain natural arch in lower back",
                "Drive through your feet for stability"
            ],
            "common_mistakes": [
                "Bouncing bar off chest",
                "Flaring elbows too wide",
                "Lifting hips off bench"
            ]
        },
        "Incline Dumbbell Press": {
            "description": "Targets the upper chest muscles while also engaging shoulders and triceps.",
            "difficulty": "Intermediate",
            "target_muscles": ["Upper Chest", "Shoulders", "Triceps"],
            "video_url": "https://www.youtube.com/watch?v=0G2_XV7slIg",
            "instructions": [
                "Set bench to 30-45 degree angle",
                "Hold dumbbells at chest level",
                "Press weights up until arms are extended",
                "Lower weights back to chest with control",
                "Keep core engaged throughout movement"
            ],
            "sets": "3-4",
            "reps": "10-12",
            "rest": "60 sec",
            "tips": [
                "Keep elbows at 45-degree angle",
                "Maintain neutral wrist position",
                "Focus on upper chest contraction"
            ],
            "common_mistakes": [
                "Using too much shoulder involvement",
                "Arching back excessively",
                "Not maintaining proper elbow angle"
            ]
        }
    },
    "Back": {
        "Pull-Ups": {
            "description": "A challenging bodyweight exercise that builds upper back and lat strength.",
            "difficulty": "Intermediate",
            "target_muscles": ["Lats", "Upper Back", "Biceps"],
            "video_url": "https://www.youtube.com/watch?v=eGo4IYlbE5g",
            "instructions": [
                "Grip bar slightly wider than shoulder width",
                "Hang with arms fully extended",
                "Pull body up until chin clears bar",
                "Lower back down with control",
                "Keep core engaged throughout"
            ],
            "sets": "3-4",
            "reps": "8-12",
            "rest": "90 sec",
            "tips": [
                "Focus on pulling with back muscles",
                "Keep shoulders down and back",
                "Maintain hollow body position"
            ],
            "common_mistakes": [
                "Using momentum to swing up",
                "Not going through full range of motion",
                "Rounding shoulders forward"
            ]
        },
        "Bent Over Rows": {
            "description": "A compound exercise that targets the entire back while also engaging biceps and core.",
            "difficulty": "Intermediate",
            "target_muscles": ["Back", "Biceps", "Core"],
            "video_url": "https://www.youtube.com/watch?v=G8l_8chR5BE",
            "instructions": [
                "Bend at hips and knees, back straight",
                "Hold barbell with overhand grip",
                "Pull bar to lower chest",
                "Lower bar with control",
                "Keep back straight throughout"
            ],
            "sets": "4",
            "reps": "10-12",
            "rest": "60 sec",
            "tips": [
                "Keep chest up and back flat",
                "Squeeze shoulder blades together",
                "Maintain neutral spine"
            ],
            "common_mistakes": [
                "Rounding back",
                "Using momentum to pull weight",
                "Not maintaining proper hip hinge"
            ]
        },
        "Lat Pulldowns": {
            "description": "An effective machine exercise for building lat width and back thickness.",
            "difficulty": "Beginner",
            "target_muscles": ["Lats", "Upper Back", "Biceps"],
            "video_url": "https://www.youtube.com/watch?v=CAwf7n6Luuc",
            "instructions": [
                "Sit with thighs under pads",
                "Grip bar wider than shoulders",
                "Pull bar down to upper chest",
                "Control bar back up",
                "Keep chest up throughout"
            ],
            "sets": "3-4",
            "reps": "12-15",
            "rest": "60 sec",
            "tips": [
                "Focus on pulling with back muscles",
                "Keep elbows pointed down",
                "Maintain upright posture"
            ],
            "common_mistakes": [
                "Leaning back too far",
                "Using momentum",
                "Not going through full range of motion"
            ]
        }
    },
    "Legs": {
        "Squats": {
            "description": "The king of leg exercises, targeting quads, hamstrings, and glutes while building overall lower body strength.",
            "difficulty": "Intermediate",
            "target_muscles": ["Quads", "Hamstrings", "Glutes", "Core"],
            "video_url": "https://www.youtube.com/watch?v=YaXPRqUwItQ",
            "instructions": [
                "Stand with feet shoulder-width apart",
                "Keep chest up and core tight",
                "Bend knees and hips to lower down",
                "Keep knees aligned with toes",
                "Drive through heels to stand up"
            ],
            "sets": "4",
            "reps": "8-12",
            "rest": "90 sec",
            "tips": [
                "Keep weight in heels",
                "Maintain neutral spine",
                "Breathe properly throughout"
            ],
            "common_mistakes": [
                "Knees caving inward",
                "Rounding back",
                "Not going deep enough"
            ]
        },
        "Romanian Deadlifts": {
            "description": "An excellent exercise for hamstrings and glutes, with emphasis on hip hinge movement.",
            "difficulty": "Intermediate",
            "target_muscles": ["Hamstrings", "Glutes", "Lower Back"],
            "video_url": "https://www.youtube.com/watch?v=GYhlG5rZpv0",
            "instructions": [
                "Stand with feet hip-width apart",
                "Hold bar with overhand grip",
                "Hinge at hips, keeping back straight",
                "Lower bar along legs",
                "Return to standing position"
            ],
            "sets": "3-4",
            "reps": "10-12",
            "rest": "90 sec",
            "tips": [
                "Keep bar close to body",
                "Maintain slight knee bend",
                "Focus on hip hinge movement"
            ],
            "common_mistakes": [
                "Rounding back",
                "Bending knees too much",
                "Not maintaining proper hip hinge"
            ]
        },
        "Bulgarian Split Squats": {
            "description": "A unilateral exercise that builds leg strength and improves balance.",
            "difficulty": "Intermediate",
            "target_muscles": ["Quads", "Glutes", "Hamstrings"],
            "video_url": "https://www.youtube.com/watch?v=2C-uNgKwPLE",
            "instructions": [
                "Stand facing away from bench",
                "Place one foot on bench behind you",
                "Lower body until front thigh is parallel to ground",
                "Drive through front heel to stand up",
                "Keep torso upright"
            ],
            "sets": "3",
            "reps": "10-12 each leg",
            "rest": "60 sec",
            "tips": [
                "Keep front knee aligned with toes",
                "Maintain upright posture",
                "Focus on controlled movement"
            ],
            "common_mistakes": [
                "Leaning too far forward",
                "Not going deep enough",
                "Losing balance"
            ]
        }
    },
    "Shoulders": {
        "Overhead Press": {
            "description": "A compound exercise that builds shoulder strength and size.",
            "difficulty": "Intermediate",
            "target_muscles": ["Shoulders", "Triceps", "Upper Chest"],
            "video_url": "https://www.youtube.com/watch?v=2yjwXTZQDDI",
            "instructions": [
                "Stand with feet shoulder-width apart",
                "Hold bar at shoulder level",
                "Press bar overhead until arms are straight",
                "Lower bar back to shoulders",
                "Keep core engaged throughout"
            ],
            "sets": "4",
            "reps": "8-12",
            "rest": "90 sec",
            "tips": [
                "Keep core tight",
                "Maintain neutral spine",
                "Breathe properly"
            ],
            "common_mistakes": [
                "Arching back",
                "Not going through full range of motion",
                "Using momentum"
            ]
        },
        "Lateral Raises": {
            "description": "An isolation exercise that targets the lateral deltoids.",
            "difficulty": "Beginner",
            "target_muscles": ["Lateral Deltoids"],
            "video_url": "https://www.youtube.com/watch?v=3VcKaXpzqRo",
            "instructions": [
                "Stand with dumbbells at sides",
                "Raise arms out to sides until parallel to ground",
                "Lower weights with control",
                "Keep slight bend in elbows",
                "Maintain upright posture"
            ],
            "sets": "3-4",
            "reps": "12-15",
            "rest": "60 sec",
            "tips": [
                "Keep wrists neutral",
                "Focus on shoulder movement",
                "Control the weight"
            ],
            "common_mistakes": [
                "Using momentum",
                "Raising arms too high",
                "Shrugging shoulders"
            ]
        },
        "Face Pulls": {
            "description": "An excellent exercise for rear deltoids and upper back health.",
            "difficulty": "Beginner",
            "target_muscles": ["Rear Deltoids", "Upper Back"],
            "video_url": "https://www.youtube.com/watch?v=rep-qVOkqgk",
            "instructions": [
                "Use rope attachment on cable machine",
                "Pull rope towards face",
                "Separate hands as you pull",
                "Squeeze shoulder blades together",
                "Return to starting position"
            ],
            "sets": "3",
            "reps": "15-20",
            "rest": "60 sec",
            "tips": [
                "Keep elbows high",
                "Focus on rear deltoid contraction",
                "Maintain upright posture"
            ],
            "common_mistakes": [
                "Using too much weight",
                "Not separating hands enough",
                "Rounding shoulders forward"
            ]
        }
    },
    "Arms": {
        "Bicep Curls": {
            "description": "A classic isolation exercise for building bicep size and strength.",
            "difficulty": "Beginner",
            "target_muscles": ["Biceps", "Forearms"],
            "video_url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
            "instructions": [
                "Stand with dumbbells at sides",
                "Curl weights up towards shoulders",
                "Lower weights with control",
                "Keep elbows close to body",
                "Maintain upright posture"
            ],
            "sets": "3-4",
            "reps": "12-15",
            "rest": "60 sec",
            "tips": [
                "Keep wrists straight",
                "Focus on bicep contraction",
                "Control the negative"
            ],
            "common_mistakes": [
                "Swinging weights",
                "Moving elbows forward",
                "Using momentum"
            ]
        },
        "Tricep Pushdowns": {
            "description": "An effective isolation exercise for triceps using a cable machine.",
            "difficulty": "Beginner",
            "target_muscles": ["Triceps"],
            "video_url": "https://www.youtube.com/watch?v=2-LAMcpzODU",
            "instructions": [
                "Stand facing cable machine",
                "Grip bar with overhand grip",
                "Push bar down until arms are straight",
                "Return to starting position",
                "Keep elbows close to body"
            ],
            "sets": "3-4",
            "reps": "12-15",
            "rest": "60 sec",
            "tips": [
                "Keep elbows stationary",
                "Focus on tricep contraction",
                "Maintain upright posture"
            ],
            "common_mistakes": [
                "Moving elbows forward",
                "Using momentum",
                "Not going through full range of motion"
            ]
        },
        "Hammer Curls": {
            "description": "A variation of bicep curls that also targets the forearms.",
            "difficulty": "Beginner",
            "target_muscles": ["Biceps", "Forearms"],
            "video_url": "https://www.youtube.com/watch?v=zC3nLlEvin4",
            "instructions": [
                "Stand with dumbbells at sides",
                "Keep palms facing each other",
                "Curl weights up towards shoulders",
                "Lower weights with control",
                "Keep elbows close to body"
            ],
            "sets": "3",
            "reps": "12-15",
            "rest": "60 sec",
            "tips": [
                "Maintain neutral grip",
                "Focus on controlled movement",
                "Keep wrists straight"
            ],
            "common_mistakes": [
                "Swinging weights",
                "Moving elbows forward",
                "Using momentum"
            ]
        }
    },
    "Core": {
        "Plank": {
            "description": "A fundamental core exercise that builds stability and endurance.",
            "difficulty": "Beginner",
            "target_muscles": ["Core", "Shoulders", "Glutes"],
            "video_url": "https://www.youtube.com/watch?v=pSHjTRCQxIw",
            "instructions": [
                "Start in push-up position",
                "Bend elbows to rest on forearms",
                "Keep body in straight line",
                "Engage core and glutes",
                "Hold position"
            ],
            "sets": "3",
            "reps": "30-60 sec",
            "rest": "60 sec",
            "tips": [
                "Keep neck neutral",
                "Don't let hips sag",
                "Breathe steadily"
            ],
            "common_mistakes": [
                "Sagging hips",
                "Raising hips too high",
                "Holding breath"
            ]
        },
        "Russian Twists": {
            "description": "An effective exercise for oblique muscles and core rotation.",
            "difficulty": "Intermediate",
            "target_muscles": ["Obliques", "Core"],
            "video_url": "https://www.youtube.com/watch?v=wkD8rjkodUI",
            "instructions": [
                "Sit on floor with knees bent",
                "Lean back slightly",
                "Rotate torso from side to side",
                "Keep core engaged",
                "Maintain balance"
            ],
            "sets": "3",
            "reps": "20-30",
            "rest": "60 sec",
            "tips": [
                "Keep back straight",
                "Move slowly and controlled",
                "Focus on rotation"
            ],
            "common_mistakes": [
                "Using momentum",
                "Rounding back",
                "Moving too quickly"
            ]
        },
        "Hanging Leg Raises": {
            "description": "An advanced core exercise that targets lower abs and hip flexors.",
            "difficulty": "Advanced",
            "target_muscles": ["Lower Abs", "Hip Flexors"],
            "video_url": "https://www.youtube.com/watch?v=JB2oyawG9KI",
            "instructions": [
                "Hang from pull-up bar",
                "Raise legs to parallel",
                "Lower legs with control",
                "Keep core engaged",
                "Avoid swinging"
            ],
            "sets": "3",
            "reps": "10-15",
            "rest": "90 sec",
            "tips": [
                "Keep legs straight",
                "Control the movement",
                "Focus on lower abs"
            ],
            "common_mistakes": [
                "Using momentum",
                "Bending knees too much",
                "Swinging body"
            ]
        }
    },
    "Full Body": {
        "Burpees": {
            "description": "A high-intensity exercise that combines strength and cardio.",
            "difficulty": "Intermediate",
            "target_muscles": ["Full Body", "Cardio"],
            "video_url": "https://www.youtube.com/watch?v=TU8QYVW0gDU",
            "instructions": [
                "Start standing",
                "Drop into push-up position",
                "Perform push-up",
                "Jump feet forward",
                "Jump up with arms overhead"
            ],
            "sets": "3",
            "reps": "10-15",
            "rest": "60 sec",
            "tips": [
                "Maintain proper form",
                "Land softly",
                "Keep core engaged"
            ],
            "common_mistakes": [
                "Skipping push-up",
                "Poor landing form",
                "Not going through full range"
            ]
        },
        "Turkish Get-Up": {
            "description": "A complex full body exercise that improves strength, stability, and mobility.",
            "difficulty": "Advanced",
            "target_muscles": ["Shoulders", "Core", "Legs", "Hip Flexors"],
            "video_url": "https://www.youtube.com/watch?v=0bWRPC49-KI",
            "instructions": [
                "Lie on back holding weight overhead",
                "Roll to elbow while keeping arm vertical",
                "Push up to seated position",
                "Sweep back leg through to half-kneeling",
                "Stand up while maintaining weight overhead"
            ],
            "sets": "3",
            "reps": "5-8 each side",
            "rest": "90 sec",
            "tips": [
                "Keep eyes on weight",
                "Move slowly and controlled",
                "Maintain vertical arm"
            ],
            "common_mistakes": [
                "Losing arm alignment",
                "Rushing the movement",
                "Poor weight control"
            ]
        },
        "Kettlebell Swings": {
            "description": "A dynamic exercise that builds power and endurance.",
            "difficulty": "Intermediate",
            "target_muscles": ["Hips", "Core", "Shoulders"],
            "video_url": "https://www.youtube.com/watch?v=YSxHifyI6s8",
            "instructions": [
                "Stand with feet shoulder-width apart",
                "Hold kettlebell with both hands",
                "Hinge at hips and swing kettlebell back",
                "Drive hips forward to swing kettlebell up",
                "Control the swing back down"
            ],
            "sets": "3",
            "reps": "15-20",
            "rest": "60 sec",
            "tips": [
                "Use hip drive, not arms",
                "Keep back straight",
                "Maintain proper breathing"
            ],
            "common_mistakes": [
                "Using arms too much",
                "Rounding back",
                "Not using proper hip hinge"
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