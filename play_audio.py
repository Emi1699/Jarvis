import requests
import time
import config
import pygame
from gtts import gTTS
import json
import os
from google.cloud import texttospeech
# import playsound
# from txtai.pipeline import TextToSpeech
# import librosa.display
# import soundfile as sf
# from IPython.display import Audio, display
# import win32com.client as wincom
# from pydub import AudioSegment
# from pydub.playback import play
# import pyttsx3
# import pythoncom

"""Option to choose between voice of {'ELEVENLABS', 'GOOGLE_CLOUD', 'gTTS', 'pyttsx3'}. 
    gTTS is free and currently much easier to hold a conversation with in real time, and is free.
    ElevenLabs and Google Cloud require API keys. Pyttsx3 is low quality."""

VOICE_ID = config.VOICE_ID
ELEVENLABS_API_KEY = config.ELEVENLABS_API_KEY
GOOGLE_CLOUD_KEYFILE_LOCATION = config.GOOGLE_CLOUD_KEYFILE

run_settings_location = "run_data/run_settings.json"
if os.path.exists(run_settings_location):
    with open(run_settings_location, 'r', encoding='utf-8') as file:
        file_contents = json.load(file)
VOICE_PROGRAM = file_contents["voice_program"]

def text_to_audio(text="Hello, world! How's it going?",language='en'):
    """
    :param text: str of text to convert to audio
    :return: str of "directory/filename.mp3"
    """
    dir_name = "mp3_responses/"
    file_name = f"prompt_response_{int(time.time())}.mp3"

    if text[0] == ">":
        text = text[1:]

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

    elif VOICE_PROGRAM == "gTTS": # medium quality, fast (Google Text to Speech)
        tts = gTTS(text, lang='en')
        tts.save(dir_name+file_name)
        # sound = AudioSegment.from_file(dir_name+file_name)

    elif VOICE_PROGRAM == "GOOGLE_CLOUD":
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_CLOUD_KEYFILE_LOCATION
        client = texttospeech.TextToSpeechClient()
        input_text = text
        synthesis_input = texttospeech.SynthesisInput(text=input_text)
        if language == 'vi':
            lang_code = 'vi-VN'
            name_code = 'vi-VN-Standard-B'
        elif language == 'es':
            lang_code = 'es-ES'
            name_code = 'es-ES-Standard-B'
        elif language == 'de':
            lang_code = 'de-DE'
            name_code = 'de-DE-Standard-B'
        elif language == 'fr':
            lang_code = 'fr-FR'
            name_code = 'fr-FR-Standard-B'
        elif language == 'zh-cn':
            lang_code = 'yue-HK'
            name_code = 'yue-HK-Standard-B'
        elif language == 'nl':
            lang_code = 'nl-NL'
            name_code = 'nl-NL-Standard-B'
        elif language == 'ru':
            lang_code = 'ru-RU'
            name_code = 'ru-RU-Standard-B'
        else:
            lang_code = 'en-US'
            name_code = 'en-GB-Standard-B'

        voice = texttospeech.VoiceSelectionParams(
            language_code = lang_code,
            name = name_code
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        with open(dir_name+file_name, 'wb') as out:
            out.write(response.audio_content)

    # elif VOICE_PROGRAM == "pyttsx3": # low quality, fast
    #     pythoncom.CoInitialize()
    #     engine = pyttsx3.init()
    #     engine.say(text)
    #     engine.save_to_file(text, dir_name+file_name)
    #     engine.runAndWait()

    # play the audio file
    pygame.init()
    pygame.mixer.music.load(dir_name+file_name)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    return dir_name+file_name