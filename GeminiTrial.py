import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API with the API key
api_key = os.getenv("GEMINI_API_KEY")
# Assuming 'genai' is properly imported and has a method 'configure' and 'GenerativeModel'
import google.generativeai as genai
genai.configure(api_key=api_key)

# Initialize the chat session and history if not already in session state
if 'chat_session' not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []
    st.session_state.subject = None

def handle_chat(question):
    try:
        response = st.session_state.chat_session.send_message(question)
        st.session_state.chat_history.append({"type": "Question", "content": question, "subject": st.session_state.subject})
        st.session_state.chat_history.append({"type": "Response", "content": response.text})
        return response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None



# Streamlit layout and input for user interaction
st.set_page_config(page_title="Quiz Bot")
st.header("🤖 Quiz Bot")

# Subject selection
subject_option = st.selectbox(
    'Choose a subject for your quiz:',
    ('Select a Subject', 'History', 'Math', 'Science'),
    index=0
)

if subject_option != 'Select a Subject':
    st.session_state.subject = subject_option
    # User input for the quiz question
    user_input = st.text_input("Type your quiz question here:")
    # Button to send the message
    if st.button("Send"):
        if user_input:
            response = handle_chat(user_input, st.session_state.subject)
            if response:
                st.write("Bot:", response.text)
        else:
            st.warning("Please type a question or message to send to the quiz bot.")
else:
    st.session_state.subject = None
    st.info("Please select a subject to continue.")

# Display chat history
st.subheader("Chat History:")
for entry in st.session_state.chat_history:
    if entry['type'] == "Question":
        st.markdown(f"**You asked about {entry['subject']}:** {entry['content']}")
    elif entry['type'] == "Response":
        st.markdown(f"**Bot replied:** {entry['content']}")

# Button to reset the conversation
# Assuming you're handling subject context manually within your application now
if st.button("Send"):
    if user_input:
        # Call handle_chat with only one argument
        response = handle_chat(user_input)  # Removed the second argument
        if response:
            st.write("Bot:", response.text)
    else:
        st.warning("Please type a question or message to send to the quiz bot.")
