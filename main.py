import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import time
import pyjokes
import requests
import cv2
import threading
import sys

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set voice rate
engine.setProperty('rate', 150)

# Global flag and lock to control video playback
video_lock = threading.Lock()
current_video_thread = None
stop_video_event = threading.Event()

# Function to play video in a window with fixed size
def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    cv2.namedWindow('Lumos', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Lumos', cv2.WND_PROP_TOPMOST, 1)
    cv2.resizeWindow('Lumos', 400, 400)  # Set the window size

    while cap.isOpened():
        if stop_video_event.is_set():
            break
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (400, 400))
        cv2.imshow('Lumos', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for 'Esc'
            break

    cap.release()
    cv2.destroyAllWindows()


# Function to start video playback in a separate thread
def start_video(video_path):
    global current_video_thread
    with video_lock:
        stop_video_event.set()  # Stop any currently playing video
        if current_video_thread:
            current_video_thread.join()  # Wait for the current video thread to finish
        stop_video_event.clear()
        current_video_thread = threading.Thread(target=play_video, args=(video_path,), daemon=True)
        current_video_thread.start()


# Function to stop video playback
def stop_video():
    stop_video_event.set()


# Function to speak and print Lumos' response
def speak(text):
    stop_video()  # Ensure any previous video is stopped
    start_video("speaking.mp4")

    lumos_text = f"Lumos: {text}"
    print(lumos_text)  # Display Lumos' response in the console
    engine.say(text)
    engine.runAndWait()

    stop_video()  # Stop the speaking video


# Function to listen for commands and print user's command
def listen_command():
    stop_video()  # Ensure any previous video is stopped
    start_video("listen.mp4")

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    stop_video()  # Stop the listening video

    try:
        command = recognizer.recognize_google(audio)
        user_text = f"User: {command}"
        print(user_text)  # Display user's command in the console
        return command.lower()
    except sr.UnknownValueError:
        #speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Sorry, I am unable to process your request.")
        return ""


# Function to get weather information
def get_weather():
    api_key = "your_openweathermap_api_key"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "your_city_name"  # Replace with your city name
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    data = response.json()

    if data.get("cod") != 200:
        error_message = data.get("message", "Error retrieving weather data")
        return f"Failed to get weather data: {error_message}"

    main = data["main"]
    temperature = main["temp"]
    pressure = main["pressure"]
    humidity = main["humidity"]
    weather_desc = data["weather"][0]["description"]
    weather_report = (f"Temperature: {temperature - 273.15:.2f}°C\n"
                      f"Pressure: {pressure} hPa\n"
                      f"Humidity: {humidity}%\n"
                      f"Description: {weather_desc}")
    return weather_report


# Function to process commands
def process_command(command):
    if "open chrome" in command:
        speak("Opening Chrome")
        webbrowser.open("http://www.google.com")
    elif "open file explorer" in command:
        speak("Opening File Explorer")
        os.system("explorer")
    elif "open whatsapp" in command:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")
    elif "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif "open my youtube channel" in command:
        speak("Opening your youtube channel")
        webbrowser.open("https://l.instagram.com/?u=https%3A%2F%2Fwww.youtube.com%2Fchannel%2FUCGBIJ4Lg-1jXLUgxb34R34A&e=AT10Z0YoyLwvfYeD8DVqKP04tEMoICG8TZnTifMTj0ljeEeFo0szN57SSQUL3TuCoiZzS0mRfE0kR1iYyzpjjRPl5M49JcFqaE0xegm5rIFC9Z7Bpa_exrI")
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "open edge" in command:
        speak("Opening Microsoft Edge")
        os.system("start msedge")
    elif "open settings" in command:
        speak("Opening Settings")
        os.system("start ms-settings:")
    elif "open vs code" in command:
        speak("Opening Visual Studio Code")
        os.system("code")
    elif "open devc++" in command:
        speak("Opening Dev-C++")
        os.system("start devcpp")
    elif "open control panel" in command:
        speak("Opening Control Panel")
        os.system("control")
    elif "weather" in command:
        speak("Getting weather information")
        weather_info = get_weather()
        speak(weather_info)
    elif "tell me a joke" in command:
        speak("Here's a joke for you")
        joke = pyjokes.get_joke()
        speak(joke)
    elif "how are you" in command:
        speak("I'm doing well, thanks for asking! How about you?")
    elif "describe yourself" in command:
        speak("I'm your virtual assistant, designed to help you with various tasks like setting reminders, managing your schedule, and providing information.")
    elif "i am fine" in command:
        speak("That's great to hear! Is there anything I can assist you with?")
    elif "set a timer" in command:
        speak("For how many seconds?")
        duration = listen_command()
        if duration.isdigit():
            speak(f"Setting a timer for {duration} seconds")
            time.sleep(int(duration))
            speak("Time's up!")
        else:
            speak("Invalid duration")
    elif "set an alarm" in command:
        speak("Please tell me the time to set the alarm. For example, say 'set alarm at 6:30 AM'.")
        alarm_time = listen_command()
        if alarm_time:
            try:
                alarm_hour, alarm_minute = map(int, alarm_time.split(" ")[2].split(":"))
                period = alarm_time.split(" ")[3].lower()
                if period == "pm" and alarm_hour != 12:
                    alarm_hour += 12
                elif period == "am" and alarm_hour == 12:
                    alarm_hour = 0
                while True:
                    current_time = datetime.datetime.now()
                    if current_time.hour == alarm_hour and current_time.minute == alarm_minute:
                        speak("Wake up! It's time to start your day!")
                        break
            except ValueError:
                speak("Sorry, I couldn't set the alarm. Please try again.")
    #else:
        #speak("Sorry, I don't understand that command.")

# Main loop
def main():
    speak("Hello Atul, Lumos is ready. Say your password to start.")
    while True:
        command = listen_command()
        if "code maker" in command:
            speak("Your password verification successful")
            speak("How can I assist you?")
            while True:
                user_command = listen_command()
                if "complete" in user_command:
                    speak("Stopping. Goodbye!")
                    return
                process_command(user_command)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop_video()
        print("Exiting program...")
        sys.exit(0)
