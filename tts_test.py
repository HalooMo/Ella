import torch
from IPython.display import display
from IPython.display import Audio
import soundfile as sf
import pygame as pg
import time


language = 'ru'
model_id = 'v4_ru'
device = torch.device('cpu')

model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
model.to(device)  # gpu or cpu

sample_rate = 48000
speaker = 'kseniya'
put_accent=True
put_yo=True
example_text = '5'

audio = model.apply_tts(text=example_text,
                        speaker=speaker,
                        sample_rate=sample_rate,
                        put_accent=put_accent,
                        put_yo=put_yo)

sf.write('aux.wav', audio, sample_rate)


pg.init()
pg.mixer.init()
pg.mixer.music.load(r"aux.wav")
pg.mixer.music.play()

while pg.mixer.music.get_busy():
    time.sleep(0.1)