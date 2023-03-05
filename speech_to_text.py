import whisper

def convert_speech_to_text(mp3_file_path, mode):
    """
    Here, we will be using openai to make the API call to convert speech to text.
    :param mp3_file_path: str
    :param mode: str with value "transcribe" or "translate" depending on the wanted usage
    :return: text of input user audio file
    """
    model_size = "small"#"large-v2"
    # if "tiny" in model_size.lower() or "base" in model_size.lower() or "small" in model_size.lower():
    #     print("Running on CPU due to small model size.")
    #     devices = torch.device("cpu")
    # else:
    #     if torch.cuda.is_available(): print("CUDA-enabled GPU detected. Using GPU.")
    #     devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # print(f"Trying to use filepath:{mp3_file_path}")
    devices = "cpu"
    model = whisper.load_model(model_size, device=devices)

    if mode=="transcribe":
        transcript = model.transcribe(mp3_file_path)
    if mode=="translate":
        transcript = model.translate(mp3_file_path)

    return transcript['text']
