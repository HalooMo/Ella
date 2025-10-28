import os


def destroy_speechs():
    try:
        for item in os.listdir(r"audio_frase"):
            os.remove(os.path.join("audio_frase", item))
    except Exception as e:
        print(e)

destroy_speechs()