import tkinter as tk
import modes
from backend import Agent
import threading
import os


class Jarvis(tk.Tk):
    # constants used throughout the program
    PADDING = 17
    BOX_COLOUR = 'black'
    TEXT_COLOUR = 'white'
    INPUT_TEXT_COLOUR = '#FF8C00'
    OUTPUT_TEXT_COLOUR = '#00CED1'
    UNSELECTED_BOX_OUTLINE_COLOUR = '#111111'
    SELECTED_BOX_OUTLINE_COLOUR = '#111111'

    def __init__(self):
        super().__init__()

        self.agent = Agent()

        self.WINDOW_WIDTH = int(self.winfo_screenwidth() * 0.68)
        self.WINDOW_HEIGHT = int(self.winfo_screenheight() * 0.78)
        self.BOX_RELATIVE_WIDTH = 0.063 * self.WINDOW_WIDTH
        self.INPUT_BOX_RELATIVE_HEIGHT = 0.0074 * self.WINDOW_HEIGHT
        self.OUTPUT_BOX_RELATIVE_HEIGHT = 0.0174 * self.WINDOW_HEIGHT

        # text widgets, labels, and buttons
        self.input_box = tk.Text(self, height=int(self.INPUT_BOX_RELATIVE_HEIGHT), width=int(self.BOX_RELATIVE_WIDTH),
                                 wrap=tk.WORD,
                                 font=('Source code pro', 20))
        self.input_box.configure(padx=self.PADDING, pady=self.PADDING, bg=self.BOX_COLOUR, fg=self.INPUT_TEXT_COLOUR,
                                 highlightbackground=self.UNSELECTED_BOX_OUTLINE_COLOUR,
                                 highlightcolor=self.SELECTED_BOX_OUTLINE_COLOUR,
                                 insertbackground=self.TEXT_COLOUR)

        # commands
        self.input_box.bind('<Shift-KeyPress-Return>',
                            lambda event: self.output_box.insert(tk.END, "\n"))  # add new line
        self.input_box.bind('<Return>', lambda event: self.process_input())  # generate response from Jarvis

        self.output_box = tk.Text(self, height=int(self.OUTPUT_BOX_RELATIVE_HEIGHT), width=int(self.BOX_RELATIVE_WIDTH),
                                  wrap=tk.WORD, font=('Source code pro', 20))
        self.output_box.configure(padx=self.PADDING, pady=self.PADDING, bg=self.BOX_COLOUR, fg=self.OUTPUT_TEXT_COLOUR,
                                  highlightbackground=self.UNSELECTED_BOX_OUTLINE_COLOUR,
                                  highlightcolor=self.SELECTED_BOX_OUTLINE_COLOUR,
                                  insertbackground=self.TEXT_COLOUR)

        self.input_label = tk.Label(self, text="> What would you like to know? (press <ENTER> to generate response)", font=('Source code '
                                                                                                                          'pro',
                                                                                                                      20))
        self.input_label.configure(bg=self.BOX_COLOUR, fg=self.TEXT_COLOUR)

        self.output_label = tk.Label(self, text="> Answer", font=('Source code pro', 20))
        self.output_label.configure(bg=self.BOX_COLOUR, fg=self.TEXT_COLOUR)

        self.process_button = tk.Button(self, text="> generate <", command=self.process_input)

        self.new_conversation_button = tk.Button(self, text="> new conversation <", command=self.new_conversation)

        self.response_generation_complete = True

    # def configure_main_window(self):
    #     # Bind the FocusIn and FocusOut events of input_box to on_entry_click and on_focus_out methods
    #     self.input_box.bind('<FocusIn>', self.on_entry_click)
    #     self.input_box.bind('<FocusOut>', self.on_focus_out)

    def configure_main_window(self):
        self.configure(bg='black')  # background color
        self.attributes("-alpha", 0.9)  # make it a bit transparent; higher value means less transparent
        self.title("J.A.R.V.I.S")

        self.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')

        # pack widgets inside parent widget (main_window)
        self.input_label.pack()
        self.input_box.pack()

        self.output_label.pack()
        self.output_box.pack()

        self.new_conversation_button.pack()
        # self.process_button.pack(side='bottom', fill='x') # dont display generate button


    def run(self):
        self.configure_main_window()
        self.mainloop()

    def display_text(self, txt):
        for index, char in enumerate(txt):
            # create a delay of 17 milliseconds before displaying each character
            self.after(10 * index, self.append_text, char)
            self.output_box.see("end")  # Scroll to the end

    def append_text(self, char):
        self.output_box.insert(tk.END, char)
        self.output_box.tag_configure('white')

    def process_input(self):
        if self.response_generation_complete and self.process_button.cget('state') == 'normal':
            self.response_generation_complete = False
            self.process_button.config(state=tk.DISABLED)
            self.new_conversation_button.config(state=tk.DISABLED)

            input_text = self.input_box.get("1.0", "end-1c")  # Get the text from the input box
            # self.input_box.delete('1.0', tk.END)  # clear input box

            # clear output box
            self.output_box.delete("1.0", tk.END)

            # start displaying loading message (3 dots in this case)
            def display_dots(count):
                if not self.response_generation_complete:
                    if count == 0:
                        self.output_box.delete("1.0", tk.END)
                        self.output_box.insert(tk.END, ".")
                    elif count == 1:
                        self.output_box.delete("1.0", tk.END)
                        self.output_box.insert(tk.END, "..")
                    elif count == 2:
                        self.output_box.delete("1.0", tk.END)
                        self.output_box.insert(tk.END, "...")
                    elif count == 3:
                        self.output_box.delete("1.0", tk.END)
                        self.output_box.insert(tk.END, ".")
                    self.after(150, display_dots, (count % 3) + 1)

            display_dots(1)

            # start a new thread to generate chatbot response
            threading.Thread(target=self.generate_response, args=(input_text,)).start()

    def generate_response(self, input_text):
        try:
            # generate chatbot response
            output_text = self.agent.get_response_for(input_text)
            output_text = "> " + output_text
            self.response_generation_complete = True

            # display response
            self.output_box.configure(state='normal')
            self.output_box.delete("1.0", tk.END)  # Clear the output box
            self.display_text(output_text)

            # Enable the "generate" and "new_conversation" buttons once the display_text method is done
            self.after(len(output_text) * 10, self.process_button.config, {'state': tk.NORMAL})
            self.after(len(output_text) * 10, self.new_conversation_button.config, {'state': tk.NORMAL})

        except Exception as e:
            print(e)

    def new_conversation(self):
        self.agent.first_message = True
        self.input_box.delete("1.0", tk.END)
        self.output_box.delete("1.0", tk.END)


if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()
