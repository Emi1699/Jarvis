import openai
import config
import modes
import os

openai.api_key = config.OPENAI_API_KEY

text = True

'''
    We need to clarify some things. 

    In order for our bot to make sense, it needs to have an idea of the history of our conversations.
    For that reason, we need to store each reply (both from the user and from the chatbot; for now we will store it
    in an array, might look into using a database in the future).

    There are 3 possible roles that an entity can have in a conversation:
        1. 'system' - this sets the tone of the chatbot and the way it will 'behave' (see below example)

        2. 'user' - self explanatory

        3. 'assistant' - this is the chatbot itself
'''

# this is where we will store the whole conversation between the chatbot and the user
messages = [
    {"role": "system", "content": modes.JARVIS}
]


# method that transcribes spoken language into text
def audio_text(audio):
    global messages

    audio_file = open(audio, 'rb')
    transcript = openai.Audio.transcribe('whisper-1', audio_file)

    messages.append({"role": "user", "content": transcript['text']})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response['choices'][0]['message']['content']

    # subprocess.call(['say', system_message])

    messages.append({"role": "assistant", "content": system_message})

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript + "\n\n" + response['usage']['total_tokens']


def get_jarvis_response_for(user_text):
    global messages

    # get the path of the directory containing the Python file
    file_path = os.path.dirname(os.path.realpath(__file__))

    # define the name of the directory to be created
    dir_name = "Conversations"
    convo_file_name = 'last_convo.txt'

    # define the path of the new directory
    dir_path = os.path.join(file_path, dir_name)

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # process text and write replies to file
    messages.append({"role": "user", "content": user_text})

    # clear file before writing to it
    with open(os.path.join(dir_path, convo_file_name), 'w') as fl:
        fl.close()

    # append user's reply to txt file
    with open(os.path.join(dir_path, convo_file_name), 'a') as fl:
        fl.write("> user: " + user_text + "\n\n")

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response['choices'][0]['message']['content']

    messages.append({"role": "assistant", "content": system_message})

    # append JARVIS' reply to txt file
    with open(os.path.join(dir_path, convo_file_name), 'a') as fl:
        fl.write("> J.A.R.V.I.S: " + system_message + "\n\n")

    return messages[-1]['content']  # return last message in the list, which should be the bot's response
