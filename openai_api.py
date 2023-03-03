import openai
import config
import modes

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


def text_text(user_text):
    global messages

    messages.append({"role": "user", "content": user_text})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response['choices'][0]['message']['content']

    # subprocess.call(['say', system_message])

    messages.append({"role": "assistant", "content": system_message})

    # in case we want to display the full history

    # chat_transcript = ""
    # for message in messages:
    #     if message['role'] != 'system':
    #         chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    # print(response['usage']['total_tokens'])

    return messages[-1]['content'] # return last message in the list, which should be the bot's response
