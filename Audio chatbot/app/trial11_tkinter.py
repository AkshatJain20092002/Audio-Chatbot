import tkinter as tk
import openai
from gtts import gTTS
import os
import speech_recognition as sr

openai.api_key = 'API_KEY'

def ask_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

def on_button_press():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source)

    try:
        prompt = r.recognize_google(audio)
        if prompt.lower() == "bye":
            print()
            print("Bye, tumharo din achha beete lala/lali")
        else:
            print("You said: " + prompt)
            bot_response = ask_gpt(prompt)
            print("Bot:", bot_response)

            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, "You said: " + prompt + "\n")
            output_text.insert(tk.END, "Bot: " + bot_response + "\n")

            tts = gTTS(text=bot_response, lang='en')
            tts.save("response.mp3")
            os.system("mpg321 response.mp3")
        
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

# Create the GUI
root = tk.Tk()

input_label = tk.Label(root, text="Press the button and speak:")
input_label.pack()

button = tk.Button(root, text="Speak", command=on_button_press)
button.pack()

output_text = tk.Text(root, height=10, width=50)
output_text.pack()

root.mainloop()
