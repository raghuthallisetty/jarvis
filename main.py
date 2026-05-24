import speech_recognition as sr
from google import genai
import os
import asyncio
import edge_tts
import datetime
import urllib.parse

# ==========================================
# 1. Initialize APIs & American Neural Voice
# ==========================================
gemini_client = genai.Client() 

# American Voice Options:
# "en-US-ChristopherNeural" (Deep, cinematic male)
# "en-US-GuyNeural"         (Friendly, conversational male)
# "en-US-AriaNeural"        (Professional, clear female)
VOICE = "en-US-ChristopherNeural"

def speak(text):
    """Generates free, high-quality neural audio and plays it instantly."""
    print(f"JARVIS: {text}")
    
    async def amain() -> None:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save("jarvis_response.mp3")
        
    try:
        asyncio.run(amain())
        os.system("afplay jarvis_response.mp3")
        os.remove("jarvis_response.mp3")
    except Exception as e:
        print(f"Voice Error: {e}")

# ==========================================
# 2. Voice Input (Optimized)
# ==========================================
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            print("[Processing...]")
            query = recognizer.recognize_google(audio)
            print(f"You: {query}")
            return query.lower()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return ""
        except sr.RequestError:
            speak("Sir, my network connection appears to be offline.")
            return ""

# ==========================================
# 3. The Action Brain (Deep Mac Control)
# ==========================================
def execute_system_action(command):
    """Allows JARVIS to control system applications and Mac hardware"""
    
    # 1. Hardware Control: Volume
    if "mute volume" in command or "silence" in command:
        speak("Muting all system audio, Sir.")
        os.system("osascript -e 'set volume output muted true'")
        return True
    elif "max volume" in command or "full volume" in command:
        speak("Pushing audio to maximum capacity.")
        os.system("osascript -e 'set volume output volume 100'")
        return True
        
    # 2. UI Control: Dark Mode
    elif "dark mode" in command:
        speak("Toggling the system interface theme now.")
        os.system('osascript -e \'tell app "System Events" to tell appearance preferences to set dark mode to not dark mode\'')
        return True
        
    # 3. System Control: Sleep
    elif "lock screen" in command or "go to sleep" in command:
        speak("Locking down the system. I will be here when you return, Sir.")
        os.system('pmset displaysleepnow')
        return True
        
    # 4. Web Surfing: Dynamic Google Search
    elif "search for" in command or "google" in command:
        # Extract the search query from the sentence
        search_term = command.replace("search for", "").replace("google", "").strip()
        encoded_term = urllib.parse.quote(search_term)
        speak(f"Pulling up the web results for {search_term}.")
        os.system(f'open "https://www.google.com/search?q={encoded_term}"')
        return True
        
    # 5. App Launching
    elif "open safari" in command or "open browser" in command:
        speak("Opening Safari.")
        os.system("open -a Safari")
        return True
    elif "open spotify" in command or "play music" in command:
        speak("Booting up Spotify.")
        os.system("open -a Spotify")
        return True
    elif "open terminal" in command:
        speak("Accessing the mainframe.")
        os.system("open -a Terminal")
        return True
        
    # 6. Real-Time Data (Bypassing LLM for speed)
    elif "what time is it" in command or "current time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"It is currently {current_time}, Sir.")
        return True
        
    return False

# ==========================================
# 4. Main Execution Loop
# ==========================================
def start_jarvis():
    # Updated prompt to match the new American persona
    system_instruction = (
        "You are JARVIS, a highly advanced, powerful artificial intelligence. "
        "You have full access to the user's computer systems. Speak with a smooth, "
        "confident, and exceptionally polite American demeanor. Address the user as 'Sir'. "
        "Your answers must be conversational, sharp, and practical. Never use lists, "
        "bullet points, or markdown formatting, as your output is being fed directly "
        "into a vocal synthesizer."
    )
    
    chat = gemini_client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": system_instruction}
    )
    
    speak("Systems updated. American vocal matrix loaded. How can I assist you today, Sir?")
    
    while True:
        user_input = listen_command()
        
        if not user_input:
            continue
            
        if any(word in user_input for word in ["shutdown", "power down", "goodbye"]):
            speak("Powering down all core matrices. Have a good day, Sir.")
            break
            
        # Try to execute a physical system command first
        action_taken = execute_system_action(user_input)
        
        # If no system command was triggered, ask the LLM
        if not action_taken:
            try:
                response = chat.send_message(user_input)
                speak(response.text)
            except Exception as e:
                print(f"API Error: {e}")
                speak("I'm experiencing a brief cognitive malfunction.")

if __name__ == "__main__":
    start_jarvis()