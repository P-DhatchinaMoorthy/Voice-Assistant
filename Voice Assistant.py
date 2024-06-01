import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

API_KEY = "AIzaSyBVN4FiHyg_6T1bFoZfV8nte1LmyDxBrGo"

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
    print("Conversation terminated.")

def listen():
    while True:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            question = recognizer.recognize_google(audio)
            print("You:", question)
            if question.lower() == "exit":
                exit_conversation()
                return
            response = send_message(instruction + question)
            print("Bot:", response)
            engine = pyttsx3.init()
            engine.say(response)
            engine.runAndWait()
            
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results: ", e)

print("Voice Assistant")
conversation_active = False
while True:
    if not conversation_active:
        command = input("Enter 'listen' to start: ").strip().lower()
        if command == "listen":
            conversation_active = True
            listen()
        else:
            print("Invalid command. Please try again.")
    else:
        command = input("Continue conversation or type 'exit' to terminate: ").strip().lower()
        if command == "okay bye":
            exit_conversation()
            break
        else:
            listen()
