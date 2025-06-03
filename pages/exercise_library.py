import streamlit as st
import sys
import os

# Add the parent directory to sys.path to ensure config can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import config module
try:
    import config
except ImportError:
    st.error("Error: Could not import config module. Please ensure config.py exists in the root directory.")
    st.stop()

def extract_youtube_id(url):
    """Extract YouTube video ID from URL."""
    if "youtube.com/watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return url

def get_exercise_image(exercise_name, category):
    """Get the appropriate image URL for an exercise"""
    exercise_images = {
        "Chest": {
            "Push-Ups": "https://content.artofmanliness.com/uploads/2020/11/Pushup-Re-do-1.jpg",
            "Bench Press": "https://fitnessprogramer.com/wp-content/uploads/2024/11/How-to-Bench-Press-with-Proper-Form.webp",
            "Incline Bench Press": "https://blog.myarsenalstrength.com/hs-fs/hubfs/bench%20press.jpeg",
        },
        "Back": {
            "Pull-Ups": "https://www.athleticinsight.com/wp-content/uploads/2022/09/Pull-up-08.jpg",
            "Lat Pulldowns": "https://scoutlife.org/wp-content/uploads/2021/08/latpulldowns.jpg",
            "Bent Over Rows": "https://stronglifts.com/wp-content/uploads/barbell-row-lower-back.jpg",
        },
        "Legs": {
            "Squats": "https://i.pinimg.com/736x/d8/2c/50/d82c50822dcb4edb1db8176c04442e54.jpg",
            "Bulgarian Split Squats": "https://img.livestrong.com/375/media-storage/contentlab-data/2/17/5505ab621e224ce3a712b8ae9f9abc5c.jpg",
            "Romanian Deadlifts": "https://sportscienceinsider.com/wp-content/uploads/2023/05/How-To-DB-Deadlift.png"
        },
        "Shoulders": {
            "Overhead Press": "https://stronglifts.com/wp-content/uploads/overhead-press-legs.jpg",
            "Lateral Raises": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRh5gXaeGuNHib5PlbMhJDbCKZaBXSwSDUFpg&s",
            "Face Pulls": "https://www.wearethemighty.com/wp-content/uploads/legacy/assets.rbl.ms/21126373/origin.png?strip=all&quality=85"
        },
        "Arms": {
            "Bicep Curls": "https://i.pinimg.com/564x/6b/2c/f9/6b2cf9693590bb9ba9ea1cc753550a79.jpg",
            "Tricep Pushdowns": "https://builtwithscience.com/wp-content/uploads/2018/12/Screen-Shot-2018-12-15-at-3.09.41-PM-min.png",
            "Hammer Curls": "https://www.athleticinsight.com/wp-content/uploads/2022/09/Dumbbell-Curl-13.jpg",
        },
        "Core": {
            "Plank": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSI7pYEF9068MzJrkILCvRKOXtn4phJw-4a6w&s",
            "Russian Twists": "https://www.kettlebellkings.com/cdn/shop/articles/russian_twist_with_kettlebell_5c19aa9f-c7de-4e32-bc9e-64e957d6a954.jpg?v=1742803968&width=1500",
            "Hanging Leg Raises": "https://www.hevyapp.com/wp-content/uploads/leg-raises.png",
        },
        "Full Body": {
            "Burpees": "https://runnerclick.com/wp-content/webpc-passthru.php?src=https://runnerclick.com/wp-content/uploads/2020/07/Burpees-photos.jpg&nocache=1",
            "Turkish Get-Up": "https://www.traintogether.co.uk/wp-content/uploads/2016/07/1..png",
            "Kettlebell Swings": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvGTckVNaEKQmo6LNS2e-Ra4Bf0NLCEK_5-g&s",
        }
    }

    # Placeholder image in case the exercise or category is not found
    placeholder_image = "https://www.muscleandfitness.com/wp-content/uploads/2019/05/1109-Exercise-Placeholder.jpg"

    return exercise_images.get(category, {}).get(exercise_name, placeholder_image)

def app():
    # Check if config module exists and has required data
    if not hasattr(config, 'EXERCISE_DATA'):
        st.error("Error: EXERCISE_DATA not found in config module.")
        st.stop()
    
    st.header("Exercise Library")
    
    # Add custom CSS for exercise images
    st.markdown("""
        <style>
        .exercise-image {
            width: 100%;
            max-height: 300px;
            object-fit: cover;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create two columns for the main layout
    main_col1, main_col2 = st.columns([2, 3])
    
    with main_col1:
        # Exercise categories
        exercise_category = st.selectbox(
            "Select Body Part",
            ["Chest", "Back", "Legs", "Shoulders", "Arms", "Core", "Full Body"]
        )
        
        # Video Preview Section
        st.markdown("### Video Preview")
        if 'current_video' not in st.session_state:
            st.session_state.current_video = None
            
        if st.session_state.current_video:
            st.video(st.session_state.current_video)
        else:
            st.info("Select an exercise to view demonstration")
    
    with main_col2:
        # Get exercises for selected category
        if exercise_category in config.EXERCISE_DATA:
            for exercise, details in config.EXERCISE_DATA[exercise_category].items():
                with st.expander(exercise):
                    # Exercise image using st.image
                    image_url = get_exercise_image(exercise, exercise_category)
                    try:
                        st.image(image_url, caption=exercise, use_container_width=True)
                    except:
                        st.warning(f"Could not load image for {exercise}")
                    
                    # Exercise information
                    st.markdown(f"### {exercise}")
                    st.write(f"**Description:** {details['description']}")
                    
                    # Video button
                    if 'video_url' in details:
                        video_url = details['video_url']
                        if st.button(f"Watch {exercise} Demo", key=f"btn_{exercise}"):
                            st.session_state.current_video = video_url
                    
                    # Difficulty and target muscles
                    if 'difficulty' in details:
                        st.write(f"**Difficulty:** {details['difficulty']}")
                    if 'target_muscles' in details:
                        st.write(f"**Target Muscles:** {', '.join(details['target_muscles'])}")
                    
                    # Instructions
                    st.write("\n**Instructions:**")
                    for i, instruction in enumerate(details['instructions'], 1):
                        st.write(f"{i}. {instruction}")
                    
                    # Training parameters
                    st.markdown("### Training Parameters")
                    cols = st.columns(3)
                    with cols[0]:
                        st.metric("Sets", details['sets'])
                    with cols[1]:
                        st.metric("Reps", details['reps'])
                    with cols[2]:
                        st.metric("Rest", details['rest'])
                    
                    # Tips and common mistakes
                    if 'tips' in details:
                        st.write("\n**Pro Tips:**")
                        for tip in details['tips']:
                            st.write(f"• {tip}")
                    
                    if 'common_mistakes' in details:
                        st.write("\n**Common Mistakes to Avoid:**")
                        for mistake in details['common_mistakes']:
                            st.write(f"- {mistake}")
        else:
            st.info(f"No exercises available for {exercise_category} yet. Check back later!")

if __name__ == "__main__":
    app() 