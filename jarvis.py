import tkinter as tk
import modes
import openai_api
import threading
from play_audio import text_to_audio
import pyaudio
import time
import wave
import os
import speech_to_text
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
import json

class Jarvis(tk.Tk):

    # constants used throughout the program
    PADDING = 17
    BOX_COLOUR = 'black'
    TEXT_COLOUR = 'white'
    UNSELECTED_BOX_OUTLINE_COLOUR = '#660080'
    SELECTED_BOX_OUTLINE_COLOUR = '#660080'

    def __init__(self):
        super().__init__()

        self.WINDOW_WIDTH = int(self.winfo_screenwidth() * 0.65)
        self.WINDOW_HEIGHT = int(self.winfo_screenheight() * 0.85)
        self.BOX_RELATIVE_WIDTH = 0.05 * self.WINDOW_WIDTH
        self.INPUT_BOX_RELATIVE_HEIGHT = 0.0065 * self.WINDOW_HEIGHT
        self.OUTPUT_BOX_RELATIVE_HEIGHT = 0.018 * self.WINDOW_HEIGHT

        self.font_size = 20

        # text widgets, labels, and buttons
        self.input_box = tk.Text(self, height=int(self.INPUT_BOX_RELATIVE_HEIGHT), width=int(self.BOX_RELATIVE_WIDTH),
                                 wrap=tk.WORD,
                                 font=('Source code pro', self.font_size))
        self.input_box.configure(padx=self.PADDING, pady=self.PADDING, bg=self.BOX_COLOUR, fg='gray',
                                 highlightbackground=self.UNSELECTED_BOX_OUTLINE_COLOUR,
                                 highlightcolor=self.SELECTED_BOX_OUTLINE_COLOUR,
                                 insertbackground=self.TEXT_COLOUR)

        # commands
        self.input_box.bind('<Shift-KeyPress-Return>', lambda event: self.output_box.insert(tk.END, "\n")) # add new line
        self.input_box.bind('<Return>', lambda event: self.process_input()) # generate response from Jarvis

        self.output_box = tk.Text(self, height=int(self.OUTPUT_BOX_RELATIVE_HEIGHT), width=int(self.BOX_RELATIVE_WIDTH),
                                  wrap=tk.WORD, font=('Source code pro', self.font_size))
        self.output_box.configure(padx=self.PADDING, pady=self.PADDING, bg=self.BOX_COLOUR, fg=self.TEXT_COLOUR,
                                  highlightbackground=self.UNSELECTED_BOX_OUTLINE_COLOUR,
                                  highlightcolor=self.SELECTED_BOX_OUTLINE_COLOUR,
                                  insertbackground=self.TEXT_COLOUR)

        self.input_label = tk.Label(self, text="> What would you like to know?", font=('Source code pro', self.font_size))
        self.input_label.configure(bg=self.BOX_COLOUR, fg=self.TEXT_COLOUR)

        self.output_label = tk.Label(self, text="> Answer", font=('Source code pro', self.font_size))
        self.output_label.configure(bg=self.BOX_COLOUR, fg=self.TEXT_COLOUR)

        self.process_button = tk.Button(self, text=" Submit Query ", command=self.process_input, font=('Source code pro', self.font_size))

        self.record_button = tk.Button(self, text=" Record Query ", command=self.start_recording, font=('Source code pro', self.font_size))

        self.replay_button = tk.Button(self, text=" Replay Response ", command=self.replay_response, font=('Source code pro', self.font_size))

        self.response_generation_complete = True
        self.recording = False
        self.configure_main_window()
        self.answer_file_location_list = []

        self.play_audio_boolean = False
        run_settings_location = "run_data/run_settings.json"
        if os.path.exists(run_settings_location):
            with open(run_settings_location, 'r', encoding='utf-8') as file:
                file_contents = json.load(file)
                self.play_audio_boolean = file_contents["play_audio_boolean"]

        self.chat_log = ""
        self.chat_log_start_time = int(time.time())

    def configure_main_window(self):

        self.configure(bg='black')  # background color
        self.attributes("-alpha", 0.9)  # make it a bit transparent; higher value means less transparent
        self.title("J.A.R.V.I.S")

        self.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}')

        # pack widgets inside parent widget (main_window)
        self.input_label.pack()
        self.input_box.pack()
        self.record_button.pack()

        self.output_label.pack()
        self.output_box.pack()

        self.process_button.pack()
        self.replay_button.pack()


    def run(self):
        self.configure_main_window()
        self.mainloop()

    def display_text(self, txt):
        for index, char in enumerate(txt):
            # create a delay of 17 milliseconds before displaying each character
            self.after( index, self.append_text, char)
            self.output_box.see("end")  # Scroll to the end

    def append_text(self, char):
        self.output_box.insert(tk.END, char)
        self.output_box.tag_configure('white')

    def process_input(self):
        if self.response_generation_complete and self.process_button.cget('state') == 'normal':
            self.response_generation_complete = False
            self.process_button.config(state=tk.DISABLED)

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
            self.process_button.config(state='normal')

    def generate_response(self, input_text):
        try:
            # generate chatbot response
            output_text = openai_api.text_text(input_text)
            output_text = "> " + output_text
            self.response_generation_complete = True

            print("J.A.R.V.I.S.: "+output_text)
            self.chat_log += "J.A.R.V.I.S.: "+output_text + "\n"
            with open(f"chat_logs/chat_log{self.chat_log_start_time}.txt", "w", encoding='utf-8') as file:
                file.write(self.chat_log)

            # display response
            self.output_box.configure(state='normal')
            self.output_box.delete("1.0", tk.END)  # Clear the output box
            self.display_text(output_text)

            if self.play_audio_boolean:
                self.answer_file_location_list = [text_to_audio(text=output_text)]

            # Enable the "generate" button once the display_text method is done
            self.after(len(output_text) * 10, self.process_button.config, {'state': tk.NORMAL})

        except Exception as e:
            print(e)

    def replay_response(self):
        try:
            # play the audio file using pydub
            audio_file = AudioSegment.from_file(self.answer_file_location_list[0], format="mp3")
            play(audio_file)
        except Exception as e:
            print(e)

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.input_box.delete("1.0", tk.END)
            self.record_button.config(text="> stop recording <", bg="red")
            self.input_box.config(state='disabled')
            self.process_button.config(state='disabled')
            dir_name = "mp3_queries/"
            if not os.path.exists(dir_name): os.makedirs(dir_name)
            file_name = f"prompt_response_{int(time.time())}.mp3"
            file_location = dir_name+file_name
            threading.Thread(target=self.record_audio, args=(file_location,)).start()
        else:
            self.recording = False
            self.record_button.config(text="Record", bg="SystemButtonFace")
            self.input_box.config(state='normal')
            self.process_button.config(state='normal')

    def record_audio(self, file_location):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5

        audio = pyaudio.PyAudio()

        # start recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if not self.recording:
                break
            data = stream.read(CHUNK)
            frames.append(data)

        # stop recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # save recording as wav file

        wave_file = wave.open(file_location, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
        time.sleep(1)

        # Show processed speech to text in input box.
        speech_to_text_result = speech_to_text.convert_speech_to_text(file_location, mode="transcribe")
        print("User: " + speech_to_text_result)
        self.chat_log += "User: " + speech_to_text_result+"\n"
        with open(f"chat_logs/chat_log{self.chat_log_start_time}.txt", "w", encoding='utf-8') as file:
            file.write(self.chat_log)
        self.input_box.insert(tk.END, speech_to_text_result)
        self.generate_response(speech_to_text_result)

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()