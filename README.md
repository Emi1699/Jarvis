# J.A.R.V.I.S.

Just A Really Very Intelligent System :)

Inspired by Iron-Man's sophisticated assistant.

This project is also found inside my #machine-learning repository; I started developing it there as a side-project to get some experience with OpenAI's new API, but it grew into something that I use every single day.

![jarvis](https://user-images.githubusercontent.com/20230738/226624271-230f7231-7d91-413b-99f6-8403927bf745.PNG)

## About the files

- `config.py`: Here is where you'll keep your API_KEY (see step 2-4 below).
- `jarvis.py`: GUI.
- `backend`: Consume the OpenAI API and manage the conversation files.
- `modes.py`: This sets the tone for how the chatbot responds and 'behaves' for the rest of the conversation. You can add your own modes as well. Make sure to go to line 43 inside the 'backend.py' and change that line to whatever mode you want to use.
- `categories.py`: Most common interest categories found online. You can add your own there, and JARVIS will automatically use them if he finds a conversation that matches that specific category.


## Conversation Logs

J.A.R.V.I.S. will automatically save your conversation logs into folders based on the topic being discussed. This feature will make it easier for you to locate and review your previous conversations on specific subjects. By default, J.A.R.V.I.S. will store the logs in the 'Conversations/<TOPIC_SUMMARY>' folder, where <TOPIC_SUMMARY> is decided based on the user's first message in a new conversation.

The topic are chosen from a list of 20 most common topics that people are searching for online, which are found inside the `categories.py` file.

When you press the 'new conversation' button at the bottom of the window, JARVIS will generate a new 'TOPIC_SUMMARY' file inside the 'Conversations' folder after you input the first message inside that new conversation.

## Usage

Nothing much to see here, but just wanted to remind people that they can press:

- `<return> / <enter>` -> Generate response from JARVIS
- `<return> / <enter> + <shift>` -> add new line to the input box

So it is just like any other input field out there.

Also, you might need to scroll to view JARVIS's full response (just a reminder that you can do it :D).

## System Requirements

I've tested it on Windows an MacOS and it works on both.

I have not tested it on Windows; do so at your own peril. Also, the instructions below assume you are on a UNIX-based machine.

I am using Python >= 3.7 (i have developed the app on 2 different machines, with different Python versions and it works on both).

## How to Run

### 1. Install the OpenAI Library

```
$ pip install openai
```

### 2. Get your API Key from OpenAI

Go to https://platform.openai.com/account/api-keys and create your own API key.

### 3. Create a `config.py` file

Create a `config.py` file inside the project's main folder (where `jarvis.py` resides)

```
$ touch config.py
```

### 4. Add your API Key to the Config File

Add this line inside the `config.py` file: `OPENAI_API_KEY = "your-api-key"`.

Replace `'your-api-key'` with your API key from step 2.

### 5. Run the Program

Run the program from inside the `src` directory using the following command:

```
$ python jarvis.py
```

### 6. Enjoy pretending you are Iron-Man!
