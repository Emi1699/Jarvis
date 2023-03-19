import tkinter as tk
import modes
from backend import Agent
import threading
import os
from colorama import Fore, Style


def get_user_input():
    user_input = ''

    while True:
        # get user input
        text = input("> ME: ")

        # check if only return key was used
        if text == '\r':
            # exit loop when user has finished input
            if user_input.endswith('\n'):
                break
        # check if shift+return was used
        elif '\r' in text:
            # split the input text and append each line to user_input
            lines = text.split('\r')
            for line in lines:
                user_input += line + '\n'
        else:
            user_input += text

    return user_input


class Jarvis():
    def __init__(self):
        self.agent = Agent()

    def run(self):
        while True:
            user_input = get_user_input()
            print(Fore.RED + f"{self.agent.get_response_for(user_input)}\n" + Style.RESET_ALL)


if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()