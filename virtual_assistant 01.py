import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import pyjokes
import requests
import python_weather
import os
import webbrowser
import asyncio

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set voice properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 for male, 1 for female

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice command
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, I didn't catch that. Can you repeat?")
        return "None"
    return query.lower()

# Function to greet user
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning! How can I help you?")
    elif 12 <= hour < 18:
        speak("Good afternoon! How can I help you?")
    else:
        speak("Good evening! How can I help you?")

async def get_weather(city):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city)
        return weather

# Main function
def run_assistant():
    greet()
    while True:
        query = take_command()
        
        if "wikipedia" in query:
            try:
                speak("What would you like to know from Wikipedia?")
                search_query = take_command()
                if search_query.lower() != "none":
                    speak(f"Searching Wikipedia for {search_query}...")
                    try:
                        # Set language to English and disable suggestion
                        wikipedia.set_lang("en")
                        results = wikipedia.summary(search_query, sentences=2, auto_suggest=False)
                        speak("According to Wikipedia...")
                        speak(results)
                    except wikipedia.exceptions.DisambiguationError as e:
                        options = e.options[:3]  # Get first 3 options
                        speak(f"Multiple options found. Did you mean: {', '.join(options)}?")
                    except wikipedia.exceptions.PageError:
                        speak("Sorry, I couldn't find any information on that topic.")
            except Exception as e:
                speak("Sorry, I encountered an error with Wikipedia.")
                print(f"Wikipedia search error: {e}")
        
        elif "open youtube" in query:
            speak("Opening YouTube...")
            webbrowser.open("https://youtube.com")
        
        elif "open whatsapp" in query:
            speak("Opening WhatsApp...")
            webbrowser.open("https://web.whatsapp.com")
        
        elif "open google" in query:
            speak("Opening Google...")
            webbrowser.open("https://google.com")
        
        elif "play music" in query:
            speak("Playing music on YouTube...")
            pywhatkit.playonyt("latest bollywood songs")
        
        elif "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")
        
        elif "date" in query:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today's date is {current_date}")

        elif "open telegram" in query:
            speak("Opening Telegram...")
            webbrowser.open("https://telegram.com")
        
        elif "weather" in query:
            speak("Which city's weather would you like to know?")
            city = take_command()
            if city != "None":
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    weather = loop.run_until_complete(get_weather(city))
                    speak(f"The weather in {city} is {weather.current.temperature}°C")
                except Exception as e:
                    speak("Sorry, I couldn't fetch the weather information.")
                    print(f"Weather error: {e}")
        
        elif "joke" in query:
            try:
                joke = pyjokes.get_joke()
                speak("Here's a joke for you...")
                speak(joke)
            except Exception as e:
                speak("Sorry, I couldn't find a joke right now.")
                print(f"Joke error: {e}")
        
        elif "search" in query:
            search_query = query.replace("search", "").strip()
            if search_query:
                speak(f"Searching for {search_query}...")
                pywhatkit.search(search_query)
            else:
                speak("Please tell me what to search for.")
        
        elif "exit" in query or "stop" in query or "bye" in query:
            speak("Goodbye! Have a great day.")
            break
        
        else:
            speak("Sorry, I didn't understand that. Can you repeat?")

if __name__ == "__main__":
    run_assistant()