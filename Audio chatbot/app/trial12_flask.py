from flask import Flask, render_template, request
import openai
import speech_recognition as sr
import pyttsx3

openai.api_key = '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'

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.form['prompt']
    bot_response = ask_gpt(prompt)

    engine = pyttsx3.init()
    engine.say(bot_response)
    engine.runAndWait()

    return bot_response

@app.route('/voice')
def voice():
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

            engine = pyttsx3.init()
            engine.say(bot_response)
            engine.runAndWait()
        
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
