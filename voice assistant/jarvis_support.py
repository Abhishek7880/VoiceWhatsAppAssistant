import datetime
import os
import time

import pyttsx3
import speech_recognition as sr
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys

# ------------------- CONFIG -------------------
WAKE_WORDS = ["jarvis", "hey jarvis", "Hello jarvis"]
WHATSAPP_PATH = r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2535.3.0_x64__cv1g1gvanyjgm\WhatsApp.exe"


def speak(text):
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 175)
    print(f"[Jarvis]: {text}")
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)


# ------------------- LISTEN FUNCTION -------------------
def listen(timeout=8, phrase_time_limit=12):
    r = sr.Recognizer()
    r.energy_threshold = 400  # sensitivity
    r.pause_threshold = 0.8  # gap allowed between words

    with sr.Microphone() as source:
        print("[Listening]...")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("[No speech detected]")
            return ""

    try:
        command = r.recognize_google(audio, language="en-in")
        print(f"[Heard]: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("[Unrecognized speech]")
        return ""
    except sr.RequestError:
        speak("Internet connection error.")
        return ""


def get_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning sir."
    elif 12 <= hour < 17:
        return "Good afternoon sir."
    elif 17 <= hour < 21:
        return "Good evening sir."
    else:
        return "Hello sir."


# ------------------- WHATSAPP FUNCTIONS -------------------
def wait_for_whatsapp(timeout=20):
    start_time = time.time()
    while time.time() - start_time < timeout:
        wins = Desktop(backend="uia").windows()
        for w in wins:
            if w.window_text().strip() == "WhatsApp":
                return w
        time.sleep(0.5)
    return None


def click_message_box(win):
    edits = win.descendants(control_type="Edit")
    for e in edits:
        try:
            if "Type a message" in e.get_value():
                e.click_input()
                return True
        except:
            pass
    rect = win.rectangle()
    x = rect.left + (rect.width() // 2)
    y = rect.bottom - 50
    win.click_input(coords=(x - rect.left, y - rect.top))
    return True


def send_whatsapp_message(contact_name, message):
    print("Opening WhatsApp Desktop...")

    try:
        Application(backend="uia").connect(title="WhatsApp")
    except:
        if not os.path.exists(WHATSAPP_PATH):
            print("WhatsApp Desktop not found.")
            return
        Application(backend="uia").start(WHATSAPP_PATH)

    main_win = wait_for_whatsapp()
    if not main_win:
        print("WhatsApp window did not appear in time.")
        return

    main_win.set_focus()
    time.sleep(0.8)

    # Always go to search bar & clear it
    send_keys("^f")
    time.sleep(0.3)
    send_keys("^a{BACKSPACE}")
    time.sleep(0.3)

    # Search contact
    send_keys(contact_name, with_spaces=True)
    time.sleep(0.8)

    # Move to first result & open
    send_keys("{DOWN}")
    time.sleep(0.2)
    send_keys("{ENTER}")
    time.sleep(1.0)

    # Click chat message box
    click_message_box(main_win)
    time.sleep(0.2)

    # Type & send message
    send_keys(message, with_spaces=True)
    time.sleep(0.2)
    send_keys("{ENTER}")
    print(f"Message sent to {contact_name}.")


def close_whatsapp():
    try:
        app = Application(backend="uia").connect(title="WhatsApp")
        app.kill()
        print("WhatsApp closed successfully.")
        speak("WhatsApp has been closed.")
    except:
        print("WhatsApp was not running.")
        speak("WhatsApp was not running.")


# ------------------- COMMAND EXECUTOR -------------------
def execute_command(command):
    if not command:
        return

    if "send whatsapp message" in command:
        while True:  # loop until user says close
            # ask contact
            speak("To whom should I send the message?")
            contact = listen()
            while not contact:
                speak("I didn't catch the contact name. Please say it again.")
                contact = listen()

            # ask message
            message = ""
            while not message:
                speak(f"What message do you want to send to {contact}?")
                message = listen()
                if not message:
                    speak("I still didn't catch the message. Please say it again clearly.")

            speak(f"Opening WhatsApp and sending message to {contact}.")
            send_whatsapp_message(contact, message)

            # ask for next action
            speak("Do you want to close WhatsApp or send another message?")
            action = listen()

            if "close WhatsApp" in action  or "quit" in action:
                close_whatsapp()
                break  # exit loop
            elif "send" in action or "another" in action or "message" in action:
                continue  # restart loop
            else:
                speak("I didn't understand. Closing WhatsApp for now.")
                close_whatsapp()
                break

    if any(w in command for w in ["exit", "stop", "goodbye", "ok bye"]):
        speak("Goodbye.")
    try:
        active_win = Desktop(backend="uia").get_active()
        active_win.close()
    except:
        pass
    import pyautogui
    pyautogui.hotkey('win', 'd')

    exit()
