
from backend import Agent
from colorama import Fore, Style
from system import user_os


def get_user_input():
    user_input = input("> ME: ")

    return user_input

class Jarvis():
    def __init__(self):
        self.agent = Agent()

    def run(self):
        while True:
            user_input = get_user_input()

            if user_os.get_operating_system() == 'Windows':
                print(self.agent.get_response_for(user_input))
            else:
                print(Fore.CYAN + f"{self.agent.get_response_for(user_input)}\n" + Style.RESET_ALL)


if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()