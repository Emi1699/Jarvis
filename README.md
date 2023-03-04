# J.A.R.V.I.S.

Just A Really Very Intelligent System :)

Inspired by Iron-Man's sophisticated assistant.

This project is also found inside my #machine-learning repository; I started developing it there as a side-project to get some experience with OpenAI's new API, but it grew into something that I use every single day.

Lots of improvements need to be done still, especially on the GUI side.

## About the files

- `config.py`: Here is where you'll keep your API_KEY (see step 2-4 below).
- `jarvis.py`: GUI.
- `openai_api`: Consume the OpenAI API.
- `modes.py`: This sets the tone for how the chatbot responds and 'behaves' for the rest of the conversation. You can add your own modes as well; make sure to go to line 26 in `openai_api.py` and use whatever mode you want for your app. (Read the official docs to get a better idea).

## Usage

Nothing much to see here, but just wanted to remind people that they can press:

- `<return>` -> Generate response from JARVIS
- `<return> + <shift>` -> add new line to the input box

So it is just like any other input field out there.

Also, you might need to scroll to view JARVIS's full response (just a reminder that you can do it :D).

## System Requirements

This will almost certainly work on any UNIX-like system that supports the OpenAI library.

I have not tested it on Windows; do so at your own peril. Also, the instructions below assume you are on a UNIX-based machine.

I am using Python 3.9.

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

```
$ python jarvis.py
```

### 6. Enjoy pretending you are Iron-Man!
