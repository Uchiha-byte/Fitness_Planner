import streamlit as st
from importlib import reload
import config
import sys

def extract_youtube_id(url):
    """Extract YouTube video ID from URL."""
    if "youtube.com/watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return url

def app():
    # Reload the config module to get fresh data
    if "config" in sys.modules:
        reload(config)
    
    st.header("Exercise Library")
    
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