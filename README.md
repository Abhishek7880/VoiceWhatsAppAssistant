# VoiceWhatsAppAssistant
Voice-controlled WhatsApp assistant to send messages hands-free on Windows.
# VoiceWhatsAppAssistant

A **voice-controlled WhatsApp desktop assistant** built in Python.  
It allows you to send WhatsApp messages hands-free, using voice commands. You can also choose to send multiple messages or close WhatsApp directly from the assistant.

---

## Features

- Send WhatsApp messages using voice commands.
- Send messages to multiple contacts in a loop.
- Option to close WhatsApp or keep it running after sending messages.
- Voice feedback using **pyttsx3**.
- Supports commands like "exit", "stop", "goodbye" to close the assistant safely.
- Works on **Windows** with WhatsApp Desktop installed.

---

## Supported WhatsApp Voice Commands

- **"Send WhatsApp message"** → starts the message-sending flow.  
- **"Send another message"** → send a message to a different contact without restarting the app.  
- **"Close WhatsApp"** → closes WhatsApp Desktop.  
- **"Exit / Stop / Goodbye / Ok Bye"** → closes the assistant and returns to desktop.  

---

## Requirements

- Python 3.9+
- [WhatsApp Desktop](https://www.whatsapp.com/download)
- Python libraries:
  ```bash
  pip install pyttsx3 pywinauto SpeechRecognition pyautogui pyaudio
