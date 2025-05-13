EXERCISE_DATA = {
    "Chest": {
        "Bench Press": {
            "description": "A compound exercise that primarily targets the chest muscles (pectoralis major and minor).",
            "instructions": [
                "Lie on a flat bench with feet firmly on the ground",
                "Grip the barbell slightly wider than shoulder width",
                "Lower the bar to your chest with control",
                "Press the bar back up to starting position"
            ],
            "sets": "3-4",
            "reps": "8-12",
            "rest": "90-120 seconds"
        },
        "Push-Ups": {
            "description": "A bodyweight exercise that works the chest, shoulders, and triceps.",
            "instructions": [
                "Start in a plank position with hands shoulder-width apart",
                "Lower your body until chest nearly touches the ground",
                "Push back up to starting position",
                "Keep your core tight throughout the movement"
            ],
            "sets": "3-4",
            "reps": "10-20",
            "rest": "60 seconds"
        }
    },
    "Back": {
        "Pull-Ups": {
            "description": "A compound upper body exercise that primarily targets the back muscles.",
            "instructions": [
                "Hang from a pull-up bar with hands slightly wider than shoulders",
                "Pull yourself up until chin is over the bar",
                "Lower yourself back down with control",
                "Maintain proper form throughout"
            ],
            "sets": "3-4",
            "reps": "6-12",
            "rest": "90 seconds"
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