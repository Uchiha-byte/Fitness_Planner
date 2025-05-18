# -*- coding: utf-8 -*-
"""
AI Coach Module
Provides AI-powered fitness coaching and guidance
"""

import streamlit as st
from utils import generate_ai_response
from config import OPENAI_API_KEY
import openai
from datetime import datetime

def app():
    st.header("AI Coach")
    
    # Check if API key is configured
    if OPENAI_API_KEY == "AIzaSyBLGT29OGmcA4dPxJAmHbbYPkZUScpWOI0":
        st.error("Please configure your OpenAI API key in config.py")
        return
    
    # Initialize chat history in session state if not exists
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat interface
    st.subheader("Chat with your AI Fitness Coach")
    
    # Display chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your fitness question..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            # Generate AI response
            response = generate_ai_response(prompt, context="""
            You are an AI fitness coach. Your role is to provide helpful, accurate, and motivating
            fitness advice. You can help with:
            - Exercise form and technique
            - Workout planning and modifications
            - Nutrition guidance
            - Recovery strategies
            - Goal setting and progress tracking
            
            Keep responses concise, practical, and evidence-based.
            """)
            
            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Display AI response
            with st.chat_message("assistant"):
                st.markdown(response)
        
        except Exception as e:
            st.error(f"Sorry, I encountered an error: {str(e)}")
    
    # Clear chat history button
    if st.session_state.chat_history:
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    app() 