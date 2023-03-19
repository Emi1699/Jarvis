import tkinter as tk
import modes
from backend import Agent
import threading
import os


class Jarvis(tk.Tk):

    def __init__(self):
        super().__init__()
        self.agent = Agent()


if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()
