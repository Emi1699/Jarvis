from langdetect import detect

def identify_language(text):

    language_code = detect(text)
    print("Language is "+str(language_code))

    return language_code
