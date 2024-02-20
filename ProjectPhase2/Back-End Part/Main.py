import openai
import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random

# Check if the Firebase Admin SDK has been initialized
if not firebase_admin._apps:
    # Initialize Firebase Admin SDK with service account key file
    cred = credentials.Certificate("/Users/saikarthiknaladala/Downloads/key.json")
    firebase_admin.initialize_app(cred)

# Initialize Firebase
config = {
    'apiKey': "AIzaSyDc6pG4ozv0J_Sbc9ELYSG13sTn4AYLQE4",
    'authDomain': "dscapstone-96cda.firebaseapp.com",
    'projectId': "dscapstone-96cda",
    'storageBucket': "dscapstone-96cda.appspot.com",
    'messagingSenderId': "682161845845",
    'appId': "1:682161845845:web:028a2e06fdadb6f88506dc",
    'measurementId': "G-CD6H1NV5LF",
    'databaseURL': ''  # Your Realtime Database URL if you're using it
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def insert_data(collection_name, data):
    try:
        db = firestore.client()
        db.collection(collection_name).add(data)
        return True
    except Exception as e:
        st.error(f"Failed to insert data: {e}")
        return False

st.title("UniBuddy")

#openai.api_key = st.secrets['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']

st.sidebar.title("Chat History")
collection_name = st.text_input("Collection Name")

if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])

if prompt := st.chat_input("What is up?"):


    with st.chat_message(name="user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role":"user","content":prompt})

    response = f"Echo : {prompt}"
    data = {
        "Prompt": prompt,
        "Response": response
    }
   #action = {"Prompt": prompt}
    #reaction = {"Response": response}
    insert_data(collection_name, data)
    #insert_data(collection_name, reaction)
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role":"user","content":response})
    st.session_state.chat_history.append(prompt)
    for idx, question in enumerate(reversed(st.session_state.chat_history)):
        st.sidebar.text(f"{idx + 1}. {question}")