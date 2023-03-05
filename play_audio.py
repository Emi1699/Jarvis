import requests
import playsound
import time
import config

"""Made by llfuller with much help from ChatGPT"""
VOICE_ID = config.VOICE_ID
def text_to_audio(text="Hello, world! How's it going?"):
    """
    :param text: str of text to convert to audio
    :return: str of "directory/filename.mp3"
    """

    ELEVENLABS_API_KEY = config.ELEVENLABS_API_KEY

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

    dir_name = "mp3_responses/"
    file_name = f"prompt_response_{int(time.time())}.mp3"
    with open(dir_name+file_name, 'wb') as f:
        f.write(response.content)
        time.sleep(2) # give time for the voice file to finish writing to storage before attempting to play it

    # play the audio file
    playsound.playsound(dir_name+file_name, True)

    return dir_name+file_name