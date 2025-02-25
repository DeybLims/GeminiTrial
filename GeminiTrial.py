import streamlit as st
import google.generativeai as genai

# Configure the Gemini API with the API key from Streamlit's secrets
api_key = st.secrets["GEMINI_API_KEY"]
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key is not set. Check your Streamlit secrets.")

# Initialize the chat session and history if not already in session state
if 'chat_session' not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-pro')
    try:
        st.session_state.chat_session = model.start_chat()
        st.session_state.chat_history = []
        st.session_state.subject = None
    except Exception as e:
        st.error(f"Failed to start chat session: {str(e)}")

def handle_chat(question, subject):
    try:
        response = st.session_state.chat_session.send_message(question)
        st.session_state.chat_history.append({"type": "Question", "content": question, "subject": subject})
        st.session_state.chat_history.append({"type": "Response", "content": response.text})
        return response
    except Exception as e:
        st.error(f"An error occurred while sending message: {str(e)}")
        return None

# Streamlit layout and input for user interaction
st.set_page_config(page_title="Quiz Bot")
st.header("🤖 Quiz Bot")

# Subject selection
subject_option = st.selectbox(
    'Choose a subject for your quiz:',
    ('Select a Subject', 'History', 'Math', 'Science'),
    index=0,
    key='subject_select'
)

if subject_option != 'Select a Subject':
    st.session_state.subject = subject_option
    user_input = st.text_input("Type your quiz question here:", key='user_input')
    if st.button("Send", key='send_button'):
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
if st.button("Reset Conversation", key='reset_conversation'):
    try:
        st.session_state.chat_session = model.start_chat()
        st.session_state.chat_history = []  # Clear history when resetting
        st.session_state.subject = None  # Reset subject selection
    except Exception as e:
        st.error(f"Failed to reset conversation: {str(e)}")
