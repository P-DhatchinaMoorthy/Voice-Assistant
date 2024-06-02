import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

API_KEY = "AIzaSyA8-trhcEDos1fp8UvZhC56RetZRaB0rwA"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

instruction = "In this chat, respond as if you're explaining things to a five-year-old child."

def send_message(question):
    if question.strip() == '':
        return "Please ask something."

    response = chat.send_message(instruction + question)
    return response.text

def exit_conversation():
    chat.history = []
    st.session_state['conversation_ended'] = True

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        question = recognizer.recognize_google(audio)
        st.text_area("You:", value=question, height=100)
        if question.lower() == "exit":
            exit_conversation()
            st.write("Conversation terminated. Say 'Listen' to start again.")
            return
        
        response = send_message(question)
        st.text_area("Bot:", value=response, height=100)
        
        engine = pyttsx3.init()
        engine.say(response)
        engine.runAndWait()
        
    except sr.UnknownValueError:
        st.error("Could not understand audio")
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")

st.title("Voice Assistant")

if 'conversation_ended' not in st.session_state:
    st.session_state['conversation_ended'] = False

if st.button("Listen"):
    listen()

if not st.session_state['conversation_ended']:
    if st.button("Exit Conversation"):
        exit_conversation()
        st.write("Conversation terminated. Say 'Listen' to start again.")