import openai

import categories
import config
from modes import Modes
import os

# API-key; file in which it resides is not tracked by GIT
openai.api_key = config.OPENAI_API_KEY


def generate_category_and_filename(user_first_message):
    messages = [{"role": "system", "content": Modes.ENCODER.value},
                {"role": "user", "content": user_first_message}]

    msg = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)['choices'][0]['message']['content']
    print(msg)

    category = msg[:msg.index(",")]
    summary = msg[msg.index(",") + 1:]

    return category, summary


class Agent:

    def __init__(self):
        """
            We need to clarify some things.

            In order for our bot to make sense, it needs to have an idea of the history of our conversations.
            For that reason, we need to store each reply (both from the user and from the chatbot; for now we will
            store it in an array, might look into using a database in the future).

            There are 3 possible roles that an entity can have in a conversation:
                1. 'system' - this sets the tone of the chatbot and the way it will 'behave' (see below example)

                2. 'user' - self explanatory

                3. 'assistant' - this is the chatbot itself
        """

        # this is where we will store the whole conversation between the chatbot and the user
        self.messages = [{"role": "system", "content": Modes.JARVIS_COMPANION.value}]
        # API-key; file in which it resides is not tracked by GIT
        openai.api_key = config.OPENAI_API_KEY

        '''
        Create output directories and files.
        This CERTAINLY needs improvements, but not now because it's late and I'm tired as fuck.
        '''
        # get the path of the directory containing the Python file
        self.current_working_directory = os.path.dirname(os.path.realpath(__file__))
        self.conversations_directory = self.current_working_directory + "/Conversations"

        # create the 'Conversations' directory if it does not exist
        if not os.path.exists(self.conversations_directory):
            os.mkdir(self.conversations_directory)

        # both of the following variables will be set after the user's first message
        self.output_summary = ""  # define the path of the convo file inside the above directory
        self.output_category = ""  # name of the directory where the saved convo will be

        # final output file after combining the category with the summary
        self.final_output_file = ""

        self.first_message = True  # used to set the name of the output file after the user's first message

    # call the API with the prompt from the user and save each reply to a file
    def get_response_for(self, user_text):
        # process text and write replies to file
        self.messages.append({"role": "user", "content": user_text})

        # if this was the user's first message in a conversation, create the conversation's output file
        if self.first_message:
            self.output_category, self.output_summary = generate_category_and_filename(user_text)

            # remove whitespaces and dots at the end
            if self.output_summary[-1] == ".": self.output_summary = self.output_summary[:-1]
            self.output_summary = self.output_summary.strip() + ".txt"
            self.output_summary = self.output_summary.replace(" ", "_")

            self.final_output_file = os.path.join(self.conversations_directory, self.output_category + "_" + self.output_summary)

            self.first_message = False

        # append user's reply to txt file
        with open(self.final_output_file, 'a', encoding='utf-8') as fl:
            fl.write("> user: " + user_text + "\n\n")

        # this is where we call the API
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)

        # save JARVIS' message in our local list
        system_message = response['choices'][0]['message']['content']
        self.messages.append({"role": "assistant", "content": system_message})

        # append JARVIS' reply to txt file
        with open(self.final_output_file, 'a', encoding='utf-8') as fl:
            fl.write("> J.A.R.V.I.S: " + system_message + "\n\n")


        return self.messages[-1]['content']  # return last message in the list, which should be the JARVIS' response

    # generate a filename to save the output to (just like chatGPT does) and a category chosen from a list
