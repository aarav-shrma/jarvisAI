import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import config  # Ensure this file has your API key as: api_key = "YOUR_KEY"
import google.generativeai as genai
import random

# ✅ Configure Gemini API
genai.configure(api_key=config.api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # Use 1.5-flash if 2.5 isn't available

# ✅ Function to interact with Gemini AI
def ai(prompt):
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        print("AI:", text)

        # Save to file
        os.makedirs("genai", exist_ok=True)
        filename = f"genai/prompt-{random.randint(1, 999999)}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Prompt: {prompt}\n\nResponse:\n{text}")

        return text
    except Exception as e:
        print("AI Error:", e)
        return "Sorry, I couldn't process that."

# ✅ Text-to-speech engine setup
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

# ✅ Speech input function
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        say("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        say("Sorry, I'm having trouble connecting to the speech service.")
        return ""

# ✅ Main loop
if __name__ == '__main__':
    print('Jarvis is running...')
    say("Hi, my name is Jarvis")

    while True:
        text = takecommand()
        if not text:
            continue

        text_lower = text.lower()

        if "quit" in text_lower or "exit" in text_lower:
            say("Goodbye!")
            break

        elif "the time" in text_lower:
            time_now = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir, the time is {time_now}")

        elif "the date" in text_lower:
            date_now = datetime.datetime.now().strftime("%A, %d %B %Y")
            say(f"Sir, today's date is {date_now}")

        else:
            opened = False

            # ✅ Open websites
            sites = {
                "youtube": "http://www.youtube.com",
                "wikipedia": "https://www.wikipedia.com",
                "google": "https://www.google.com",
                "instagram": "https://www.instagram.com",
                "facebook": "https://www.facebook.com",
            }

            for name, url in sites.items():
                if f"open {name}" in text_lower:
                    say(f"Opening {name}, sir...")
                    webbrowser.open(url)
                    opened = True
                    break

            # ✅ Open apps
            if not opened:
                apps = {
                    "spotify": 'start "" "spotify"',
                    "vs code": "code",
                    "chrome": "start chrome",
                    "firefox": "start firefox",
                    "whatsapp": "start whatsapp",
                    "camera": "start microsoft.windows.camera:",
                }

                for app, command in apps.items():
                    if f"open {app}" in text_lower:
                        say(f"Opening {app}, sir...")
                        os.system(command)
                        opened = True
                        break

            # ✅ If not app or site, assume it's a prompt for Gemini
            if not opened:
                say("Let me think...")
                result = ai(prompt=text)
                say(result)
