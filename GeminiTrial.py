import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API with the API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=os.getenv("API_KEY"))

# Initialize the chat session and history if not already in session state
if 'chat_session' not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-pro')  
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []

# Function to handle sending messages and receiving responses from the chatbot
def handle_chat(question):
    try:
        response = st.session_state.chat_session.send_message(question)
        st.session_state.chat_history.append({"type": "Question", "content": question})
        st.session_state.chat_history.append({"type": "Response", "content": response.text})
        return response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Streamlit layout and input for user interaction
st.set_page_config(page_title="Gemini Chatbot")
st.header("🤖 Gemini Chatbot")

# User input for the chat
user_input = st.text_input("Type your question here:")

# Button to send the message
if st.button("Send"):
    if user_input:
        response = handle_chat(user_input)
        if response:
            st.write("Bot:", response.text)
    else:
        st.write("Please type a question or message to send to the chatbot.")

# Display chat history
st.subheader("Chat History:")
for entry in st.session_state.chat_history:
    if entry['type'] == "Question":
        st.markdown(f"*You asked:* {entry['content']}")
    elif entry['type'] == "Response":
        st.markdown(f"*Bot replied:* {entry['content']}")

# Button to reset the conversation
if st.button("Reset Conversation"):
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []  # Clear history when resetting
