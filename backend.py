import openai
import config
import modes
import os
import datetime

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

'''
Create output directories and files.

This CERTAINLY needs improvements, but not now because it's late and I'm tired as fuck.
'''
dir_name = "Conversations"  # name of the directory where the saved convo will be
convo_file_name = str(datetime.datetime.now()).replace(":", "_") + '.txt'  # name of the file where the convo is stored

# get the path of the directory containing the Python file
current_working_directory = os.path.dirname(os.path.realpath(__file__))

# define the path of the new directory
dir_path = os.path.join(current_working_directory, dir_name)

# define the path of the convo file inside the above directory
file_path = os.path.join(dir_path, convo_file_name)

if not os.path.exists(dir_path):
    os.mkdir(dir_path)

    # clear file before writing to it
    with open(file_path, 'w', encoding='utf-8') as fl:
        fl.close()


def get_jarvis_response_for(user_text):
    global messages

    # process text and write replies to file
    messages.append({"role": "user", "content": user_text})

    # append user's reply to txt file
    with open(file_path, 'a', encoding='utf-8') as fl:
        fl.write("> user: " + user_text + "\n\n")

    # this is where we make call the API
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    # save JARVIS' message in our local list
    system_message = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": system_message})

    # append JARVIS' reply to txt file
    with open(file_path, 'a', encoding='utf-8') as fl:
        fl.write("> J.A.R.V.I.S: " + system_message + "\n\n")

    return messages[-1]['content']  # return last message in the list, which should be the JARVIS' response
