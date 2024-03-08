import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import speech_recognition as sr
import urllib.parse

# Set page configuration
st.set_page_config(
    page_title="Unibuddy App",
    page_icon="👋",
)

# Title
st.title("Unibuddy")
st.sidebar.success("Select a page above.")

# Check if the Firebase Admin SDK has been initialized
if not firebase_admin._apps:
    # Initialize Firebase Admin SDK with service account key file
    cred = credentials.Certificate("LoginFolder/login1.json")
    firebase_admin.initialize_app(cred)

# Firebase configuration
config = {
    'apiKey': "AIzaSyAyX1XejPVzi3VZjmHrsrFuubLZzZ-ycoE",
    'authDomain': "login-info-134a1.firebaseapp.com",
    'databaseURL': "https://login-info-134a1-default-rtdb.firebaseio.com",
    'projectId': "login-info-134a1",
    'storageBucket': "login-info-134a1.appspot.com",
    'messagingSenderId': "362592688125",
    'appId': "1:362592688125:web:75e6a093b01366ad95ab94",
    'measurementId': "G-V0F4BQRCL2" 
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# Retrieve email from URL query parameters
query_params = st.experimental_get_query_params()
if "email" in query_params:
    email = urllib.parse.unquote(query_params["email"][0])
    st.write(f"Logged in as: {email}")
    collection_name = email  # Assign email to collection_name
else:
    st.write("No email found")
    collection_name = None

# Function to insert data into Firestore
def insert_data(collection_name, data):
    try:
        db = firestore.client()
        db.collection(collection_name).add(data)
        return True
    except Exception as e:
        st.error(f"Failed to insert data: {e}")
        return False

# Function to recognize speech using microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio_data = recognizer.listen(source)
        st.success("Audio captured!")
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        st.error("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Sidebar for chat history
st.sidebar.title("Chat History")

# Initialize chat history and messages
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])

# Function to handle user input
def handle_input(input_text):
    # Display user message
    with st.chat_message(name="user"):
        st.markdown(input_text)

    # Append user message to messages list
    st.session_state.messages.append({"role":"user","content":input_text})

    # Send prompt to the 2nd code for processing
    response = "Placeholder response"  # Placeholder for actual processing
    insert_data(collection_name, {"input_text": input_text, "response": response})

    # Display response from 2nd code
    with st.chat_message("assistant"):
        st.markdown(response)

    # Append user message to chat history
    st.session_state.chat_history.append(input_text)
    for idx, question in enumerate(reversed(st.session_state.chat_history)):
        st.sidebar.text(f"{idx + 1}. {question}")

# Main search bar
st.write("How can I help you today?")

# Columns for different input methods
col1, col2, col3 = st.columns([8.6, .7, .7])

# Text input for user prompt
with col1:
    if prompt := st.chat_input("Message Unibuddy..."):
        handle_input(prompt)

# Voice input button
with col2:
    if st.button("🎙️", key="voice_button"):
        voice_input = recognize_speech()
        if voice_input:
            handle_input(voice_input)

# Image upload button
with col3:
    if st.button("📷"):
        uploaded_file = st.file_uploader("", type=["jpg", "png"])
        if uploaded_file is not None:
            # Perform image processing or analysis here
            search_query = "Image uploaded"

# Optional: Handle search action
if st.session_state.get("image_button_clicked"):
    st.write("## Perform Search")
    if st.button("Search", key="search_button"):
        handle_input(search_query)
