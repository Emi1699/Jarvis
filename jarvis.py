import tkinter as tk
import modes
from backend import Agent
import threading
import os
from colorama import Fore, Style


def get_user_input():
    user_input = input("> ME: ")

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