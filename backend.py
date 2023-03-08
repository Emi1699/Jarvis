import openai

import categories
import config
from modes import Modes
import os

# API-key; file in which it resides is not tracked by GIT
openai.api_key = config.OPENAI_API_KEY


def generate_category_and_filename(user_first_message):
    category, filename = (1, 1)

    messages = [{"role": "system", "content": Modes.ENCODER.value + "Also, assign the message to a category out of these 20: " + str(list(
        categories.Categories)) + " and return both the category and the summary in a Python tuple "
                                  "of this form: category, summary, without specifying their labels, only return the values. "
                                  "For example, do NOT return it like this: (Category: Automotive, Summary: Car operation); "
                                  "return it like this: (Automotive, Car Operation). "},
                {"role": "user", "content": user_first_message}]

    print(messages)

    msg = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)['choices'][0]['message']['content']

    print(msg)


generate_category_and_filename("triangle")

# class Agent:
#
#     def __init__(self):
#         """
#             We need to clarify some things.
#
#             In order for our bot to make sense, it needs to have an idea of the history of our conversations.
#             For that reason, we need to store each reply (both from the user and from the chatbot; for now we will
#             store it in an array, might look into using a database in the future).
#
#             There are 3 possible roles that an entity can have in a conversation:
#                 1. 'system' - this sets the tone of the chatbot and the way it will 'behave' (see below example)
#
#                 2. 'user' - self explanatory
#
#                 3. 'assistant' - this is the chatbot itself
#         """
#
#         # this is where we will store the whole conversation between the chatbot and the user
#         self.messages = [{"role": "system", "content": Modes.JARVIS}]
#
#         '''
#         Create output directories and files.
#         This CERTAINLY needs improvements, but not now because it's late and I'm tired as fuck.
#         '''
#         # get the path of the directory containing the Python file
#         self.current_working_directory = os.path.dirname(os.path.realpath(__file__))
#
#         # both of the following variables will be set after the user's first message
#         self.file_name = ""  # define the path of the convo file inside the above directory
#         self.dir_name = ""  # name of the directory where the saved convo will be
#
#         # final path of the output file
#         self.file_path = ""
#
#         self.first_message = True  # used to set the name of the output file after the user's first message
#
#     # call the API with the prompt from the user and save each reply to a file
#     def get_response_for(self, user_text):
#         # process text and write replies to file
#         self.messages.append({"role": "user", "content": user_text})
#
#         # if this was the user's first message in a conversation, create the conversation's output file
#         if self.first_message:
#             self.dir_name, self.file_name = generate_category_and_filename(user_text)
#
#             self.file_path = os.path.join(self.current_working_directory, (self.dir_name + "/" + self.file_name))
#
#             self.first_message = False
#
#         # append user's reply to txt file
#         with open(self.file_path, 'a', encoding='utf-8') as fl:
#             fl.write("> user: " + user_text + "\n\n")
#
#         # this is where we call the API
#         response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
#
#         # save JARVIS' message in our local list
#         system_message = response['choices'][0]['message']['content']
#         self.messages.append({"role": "assistant", "content": system_message})
#
#         # append JARVIS' reply to txt file
#         with open(self.file_path, 'a', encoding='utf-8') as fl:
#             fl.write("> J.A.R.V.I.S: " + system_message + "\n\n")
#
#         return self.messages[-1]['content']  # return last message in the list, which should be the JARVIS' response
#
#     # generate a filename to save the output to (just like chatGPT does) and a category chosen from a list
