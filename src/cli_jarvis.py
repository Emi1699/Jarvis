
from backend import Agent
from colorama import Fore, Style
from system import user_os


def get_user_input():
    user_input = input("> ME: ")

    return user_input

class Jarvis():
    def __init__(self):
        self.agent = Agent()
        self.ENTER = True

    def run(self):
        while True:
            user_input = input("> ME:")

            print(self.agent.get_response_for(user_input))


if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()