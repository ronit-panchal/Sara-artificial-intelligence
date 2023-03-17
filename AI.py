import speech_recognition as sr
import pyttsx3

Assistant = pyttsx3.init('sapi5')
voices = Assistant.getProperty('voices')
Assistant.setProperty('voice',voices[1].id)
Assistant.setProperty('rate',140)

#speak function

def speak(audio):

    print("   ")
    Assistant.say(audio)
    print("f: {audio}")
    
    Assistant.runAndWait()

def Takecommand():

    command = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening...')
        command.pause_threshold = 1
        audio = command.listen(source,0,8)

    try:
        print("recognizing...")
        query = command.recognize_google(audio,language="en-in")
        print(f'you said: {query}')
        
    except:
        return ""

    query = str(query)
    return query.lower()

Takecommand()

FileOpenAi = open('DataBase\ApiKeys\OpenAI.txt','r')
apikey = FileOpenAi.read()
FileOpenAi.close()

from dotenv import load_dotenv
import openai

openai.api_key = apikey

load_dotenv()
completion = openai.Completion()

chat_log_template = '''ronit : Hello, who are you?
Sara : I am doing great. How can I help ronit today?
'''

def Reply(question, chat_log=None):
    if chat_log is None:
        chat_log = chat_log_template
    prompt = f'{chat_log}ronit : {question}\nSara :'
    response = completion.create(
        prompt=prompt, engine="text-davinci-003", stop=['\nronit'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=200)
    answer = response.choices[0].text.strip()
    return answer

while True:
    query = Takecommand()
    reply = Reply(query)
    speak(reply)
    print(reply)

