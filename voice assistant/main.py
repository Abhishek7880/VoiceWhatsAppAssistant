from jarvis_support import speak, listen, get_greeting, execute_command, WAKE_WORDS


def main():
    speak("All systems functional. Jarvis is here to help you.")
    active = False

    while True:
        command = listen()
        if not command:
            continue

        if not active:
            if any(wake_word in command for wake_word in WAKE_WORDS):
                active = True
                greeting = get_greeting()
                speak(greeting)
                speak("How can I help you?")
        else:
            execute_command(command)


if __name__ == "__main__":
    main()
