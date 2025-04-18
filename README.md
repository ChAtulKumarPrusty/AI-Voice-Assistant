# 💡 Lumos - AI Voice Assistant with Video Feedback

**Lumos** is a smart, interactive desktop voice assistant that listens to your commands and responds with voice **and animated video feedback**. It can open applications, tell jokes, give weather updates, set timers or alarms, and more — all triggered by your voice. The project uses Python, speech recognition, text-to-speech, and OpenCV to deliver a fun, responsive assistant experience.

## 🎥 Features

- 🎙️ Voice Command Recognition using `speech_recognition`
- 🗣️ Text-to-Speech using `pyttsx3`
- 🌐 Open websites (Google, WhatsApp, Instagram, YouTube)
- 📂 Open local applications (Chrome, Notepad, VS Code, File Explorer, etc.)
- 🌦️ Get current weather information
- 😂 Tell jokes using `pyjokes`
- ⏱️ Set timers and alarms
- 🎞️ Show corresponding video animations during listening and speaking

## 🛠️ Technologies Used

- Python 3
- [speech_recognition](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)
- [OpenCV](https://opencv.org/)
- [pyjokes](https://pypi.org/project/pyjokes/)
- threading, datetime, requests, webbrowser, and os

## 📂 Project Structure
lumos/ │ ├── speaking.mp4 # Video played when Lumos is speaking ├── listen.mp4 # Video played when Lumos is listening ├── main.py # Main code file with all logic └── README.md # Project documentation


## 🔧 Setup Instructions

1. **Clone this repository**
   git clone https://github.com/ChAtulKumarPrusty/AI-Voice-Assistant.git
   cd AI-Voice-Assistant

Install dependencies
pip install speechrecognition pyttsx3 opencv-python pyjokes requests

Replace placeholders
In get_weather() function:
Replace "your_openweathermap_api_key" with your OpenWeatherMap API Key
Replace "your_city_name" with your actual city name

Add required video files
speaking.mp4 — Video played while Lumos speaks
listen.mp4 — Video shown when Lumos is listening
You can use any 400x400 pixel looping videos or animations of your choice

Run the assistant
python main.py

Start with voice
Say: Code Maker (This is your voice password)
Then give commands like:
"Open Chrome"
"Tell me a joke"
"Set a timer"
"Describe yourself"
"Complete" — to exit

🔐 Customization
You can change the voice password from "code maker" in the main() function.
Update or add new commands inside the process_command() function.
Replace speaking.mp4 and listen.mp4 with your own animations or GIFs (converted to mp4).

📌 To-Do / Future Ideas
Add GUI interface
Support music playback and pause commands
Integrate ChatGPT or custom AI responses
Save conversation los
Improve wake-word detection with hotword libraries

📬 Contact
Created by Atul Kumar Prusty
📧 Email: chatulprust@gmail.com

If you liked this project, don't forget to ⭐ star it and follow me for more!

---

Let me know if you'd like a `requirements.txt`, GIF demo badge, or GitHub Actions for auto-deployment.
