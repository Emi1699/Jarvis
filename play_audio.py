import requests
import playsound
import time
import config
from txtai.pipeline import TextToSpeech
import librosa.display
import soundfile as sf
from IPython.display import Audio, display
import win32com.client as wincom
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3
import pythoncom
from gtts import gTTS

"""Option to choose between voice of ElevenLabs (slow) or txtai (faster). Txtai is free and currently much easier
    to hold a conversation with."""

VOICE_ID = config.VOICE_ID
ELEVENLABS_API_KEY = config.ELEVENLABS_API_KEY
VOICE_PROGRAM = config.VOICE_PROGRAM

def text_to_audio(text="Hello, world! How's it going?"):
    """
    :param text: str of text to convert to audio
    :return: str of "directory/filename.mp3"
    """
    dir_name = "mp3_responses/"
    file_name = f"prompt_response_{int(time.time())}.mp3"

    if VOICE_PROGRAM == "ELEVENLABS": # high quality, slow
        headers = {
            'accept': 'audio/mpeg',
            'xi-api-key': ELEVENLABS_API_KEY,
            'Content-Type': 'application/json',
        }

        json_data = {
            'text': text,
        }
        # TODO: Add your voice ID in the below string
        response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/'+VOICE_ID, headers=headers,
                                 json=json_data)

        with open(dir_name+file_name, 'wb') as f:
            f.write(response.content)

        time.sleep(2)  # give time for the voice file to finish writing to storage before attempting to play it

        # play the audio file
        playsound.playsound(dir_name + file_name, True)

    elif VOICE_PROGRAM == "gTTS": # medium quality, fast (Google Text to Speech)
        tts = gTTS(text, lang='en')
        tts.save(dir_name+file_name)
        sound = AudioSegment.from_file(dir_name+file_name)
        play(sound)

    elif VOICE_PROGRAM == "pyttsx3": # low quality, fast
        pythoncom.CoInitialize()
        engine = pyttsx3.init()
        engine.say(text)
        engine.save_to_file(text, dir_name+file_name)
        engine.runAndWait()


    return dir_name+file_name