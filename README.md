# J.A.R.V.I.S

Just A Really Very Intelligent System :)

Inspired by Iron-Man's sophisticated assistant.

This project is also found inside my #machine-learning repository; I started developing it there as a side-project to get some experience with OpenAI's new API, but it grew into something that I use every single day.

Lots of improvements need to be done still, especially on the GUI side.

## Disclaimer: there's lots of files in here; the ones you're interested in are config.py, jarvis.py, openai_api.py and modes.py

#### > config.py - here is where you'll keep your API_KEY (see step 2-4 below).
#### > jarvis.py - GUI
#### > openai_api - consume the OpenAI API
#### > modes.py - I won't go into too much detail here (read the official docs to get a better idea); basically, this is the first message in a conversation and sets the tone for how the chatbot responds and 'behaves' for the rest of the conversation. You can add your own modes as well; make sure to go to to line 26 in openai_api.py and use whatever mode you want for your app.

## System Requirements

This will almost certainly work on any UNIX-like system that supports the OpenAI library.

I have not tested it on Windows; do so at your own peril. Also, the instructions below assume you are on a UNIX-based machine.

I am using python 3.9


## How to run it

#### 1. Install the OpenAI library

$ pip install openai

#### 2. Get your API_KEY from openai.com

Go to https://platform.openai.com/account/api-keys and create your own API_KEY.

#### 3. Create a config.py file inside the project's main folder (where jarvis.py resides)

$ touch config.py

#### 4. Add your API_KEY to the config file.

Add this line inside the config.py file: OPENAI_API_KEY = "your-api-key".

Replace 'your-api-key' with your API_KEY from step 2.

#### 5. Run it

$ python jarvis.py

#### 6. Enjoy pretending you are Iron-Man!
