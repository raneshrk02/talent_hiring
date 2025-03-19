import streamlit as st #type:ignore
import os
import pandas as pd #type:ignore
from datetime import datetime
from models.chatbot import HiringAssistant
from utils.data_handler import save_candidate_data
from config.config import APP_TITLE, APP_DESCRIPTION, AVATAR_ASSISTANT, AVATAR_USER

def initialize_session():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = {
            'name': None,
            'email': None,
            'phone': None,
            'experience': None,
            'position': None,
            'location': None,
            'tech_stack': [],
            'conversation_completed': False
        }
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = HiringAssistant()
    
    if 'conversation_active' not in st.session_state:
        st.session_state.conversation_active = True
    
    # Add an initial greeting if messages are empty
    if len(st.session_state.messages) == 0:
        initial_greeting = st.session_state.chatbot.get_initial_greeting()
        st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

def reset_conversation():
    """Reset the conversation"""
    st.session_state.messages = []
    st.session_state.candidate_info = {
        'name': None,
        'email': None,
        'phone': None,
        'experience': None,
        'position': None,
        'location': None,
        'tech_stack': [],
        'conversation_completed': False
    }
    st.session_state.conversation_active = True
    
    initial_greeting = st.session_state.chatbot.get_initial_greeting()
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="",
        layout="centered"
    )
    
    st.markdown("""
    <style>
    .main-header {text-align: center; margin-bottom: 30px;}
    .chat-message {padding: 15px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: flex-start;}
    .assistant {background-color: #1e1e1e; border-left: 4px solid #1565c0; color: #ffffff;}
    .user {background-color: #2c2c2c; border-left: 4px solid #388e3c; color: #ffffff;}
    .message-content {margin-left: 15px;}
    .message-container {display: flex; flex-direction: column; height: 550px; overflow-y: auto;}
    .logo-img {max-width: 150px; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)
    
    initialize_session()
    
    st.markdown('<div class="main-header"><h1>TalentScout Hiring Assistant</h1></div>', unsafe_allow_html=True)
    st.markdown(APP_DESCRIPTION)
    
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            avatar = AVATAR_ASSISTANT if message["role"] == "assistant" else AVATAR_USER
            div_class = "assistant" if message["role"] == "assistant" else "user"
            st.markdown(f"""
            <div class="chat-message {div_class}">
                <div><img src="{avatar}" width="50px"></div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # If conversation is completed, show the summary
    if st.session_state.candidate_info.get('conversation_completed', False):
        st.success("Interview session completed. Thank you for your time!")
        
        st.subheader("Collected Information")
        candidate_info = st.session_state.candidate_info
        
        info_text = f"""
        **Name:** {candidate_info['name']}  
        **Email:** {candidate_info['email']}  
        **Phone:** {candidate_info['phone']}  
        **Experience:** {candidate_info['experience']} years  
        **Position:** {candidate_info['position']}  
        **Location:** {candidate_info['location']}  
        **Tech Stack:** {', '.join(candidate_info['tech_stack'] if candidate_info['tech_stack'] else [])}  
        """
        
        st.markdown(info_text)
        
        if st.button("Start New Interview"):
            reset_conversation()
            st.rerun()
    # Otherwise, show the chat interface
    else:
        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            response, updated_info, conversation_status = st.session_state.chatbot.process_message(
                user_input, st.session_state.candidate_info, st.session_state.messages
            )
            
            st.session_state.candidate_info = updated_info
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Check if conversation is ending
            if conversation_status == "end":
                st.session_state.candidate_info['conversation_completed'] = True
                # Save data before rerun
                try:
                    save_candidate_data(st.session_state.candidate_info)
                    st.session_state.data_saved = True
                except Exception as e:
                    st.error(f"Error saving data: {str(e)}")
                    st.session_state.data_saved = False
            
            st.rerun()

if __name__ == "__main__":
    main()