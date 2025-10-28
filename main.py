import speech_recognition as sr
import pyttsx3
import queue
import threading
from llm import llm_response
import requests
import time
import torch
from IPython.display import display
from IPython.display import Audio
import soundfile as sf
import random
import pygame as pg
import os


class AssistantSpeecher():
    def __init__(self):
        self.listening = False
        self.processing = False
        self.is_stop = False
        self.is_playing = False
        self.file_is_ready = False

        pg.init()
        pg.mixer.init()

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()


        self.speech_queue = queue.Queue()
        self.llm_queue = queue.Queue()



        self.language = 'ru'
        self.model_id = 'v4_ru'
        self.device = torch.device('cpu')
        self.model, self.example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                             model='silero_tts',
                                             language=self.language,
                                             speaker=self.model_id)
        self.model.to(self.device)  # gpu or cpu


    def setup_microphone(self):
        try:
            print("Настройка микрофона")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print("Возникла ошибка при настройке микрофона"); print(e)


    def get_line(self, txt_in):
        self.sample_rate = 48000
        self.speaker = 'kseniya'
        self.put_accent = True
        self.put_yo = True
        self.example_text = txt_in
        self.text_re = ""

        self.audio = self.model.apply_tts(text=self.example_text,
                                speaker=self.speaker,
                                sample_rate=self.sample_rate,
                                put_accent=self.put_accent,
                                put_yo=self.put_yo)
        self.audio_path = f'audio_frase{os.sep}aux{random.randint(1,1000)}.wav'
        sf.write(self.audio_path, self.audio, self.sample_rate)
        return self.audio_path

    def speech_recognizer(self):
        print("Прослушивание начилось")
        while self.listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)

                def regognize():
                    try:
                        print("Распознавание началось")
                        self.text_re = self.recognizer.recognize_google(
                            audio,
                            language="ru-RU"
                        )

                        if any( step_word in self.text_re.lower() for step_word in ["стоп","остановись","остановка", "не продолжай"]):
                            print("Обнаружено стоп-слово")
                            if self.is_playing:
                                self.stop_audio()
                        else:
                            if len(self.text_re.strip())>3:
                                for i in self.text_re.split(" "):
                                    if not i.isnumeric():
                                        print("Текст добавлен в очередь")
                                        self.speech_queue.put(self.text_re)
                                    else:
                                        self.llm_queue.put("Здесь число, а я не умею работать с числами")

                    except sr.UnknownValueError:
                        print("Значения не найдены")
                    except sr.RequestError as e:
                        print("Ошибка сервера распознавания")
                        print(e)
                    except Exception as e:
                        print("Ошибка в точке - 26")
                        print(e)
                threading.Thread(target=regognize, daemon=True).start()

            except sr.WaitTimeoutError:
                continue
            except  Exception as e:
                print("Ошибка в точке - 22")
                print(e)
                time.sleep(0.1)

    def speech_llm(self):
        print("Начало обработки языковой моделью")
        while self.processing:
            try:
                text = self.speech_queue.get(timeout=1)
                if text:
                    print(f"Получен запрос с текстом {text}")
                    with open(r"C:\Users\salim\PycharmProjects\Ella\speechList.txt", "r") as f:
                        from_speech_list = f.read()
                    val = str(llm_response(from_speech_list + ". да, учти при этом мои препредыдущие запросы и ответы учти их  при ответе вот они =  " + str(text))).lower()
                    with open(r"C:\Users\salim\PycharmProjects\Ella\speechList.txt", "a") as f:
                        f.write(self.text_re + "  =>  " + val + "\n")
                    if val:
                         self.llm_queue.put(val)
            except queue.Empty:
                continue
            except Exception as e:
                print("Ошибка в точке 33")
                print(e)
                time.sleep(0.1)


    def tts_say(self):
        while self.processing:
            try:
                text = self.llm_queue.get(timeout=1)
                if text:
                    def audio_speech():
                        self.au_pth = self.get_line(str(text))
                        while not os.path.exists(self.au_pth) and not os.path.getsize(self.au_pth) > 0:
                            continue
                        time.sleep(0.1)
                        if self.is_playing:
                            print("Разговор и так запущен")
                        else:
                            print("Запуск озвучки")
                            pg.mixer.music.load(self.au_pth)
                            pg.mixer.music.play()

                            self.is_playing = True

                            while pg.mixer.music.get_busy():
                                time.sleep(0.1)

                            self.is_playing = False
                    threading.Thread(target=audio_speech).start()
            except queue.Empty:
                continue
            except Exception as e:
                print("Ошибка в точке 45")
                print(e)
                time.sleep(0.1)


    def stop_audio(self):
        if self.is_playing:
            pg.mixer.music.stop()
            self.is_playing = False
            print("Аудио остановленно")
        else:
            print("Аудио не запущено")


    def start(self):
        print("Процесс запущен")
        self.setup_microphone()

        self.listening = True
        self.processing = True

        threadings = []
        speech_thread = threading.Thread(target=self.speech_recognizer, daemon=True)
        threadings.append(speech_thread)

        llm_thread = threading.Thread(target=self.speech_llm, daemon=True)
        threadings.append(llm_thread)

        tts_thread = threading.Thread(target=self.tts_say, daemon=True)
        threadings.append(tts_thread)

        for i in threadings:
            i.start()

        print("Малый старт")
        print(f"Размер очереди распознаной речи{self.speech_queue.qsize()}")
        print(f"Размер очереди озвучиваемой речи{self.llm_queue.qsize()}")


        try:
            while self.listening:
                time.sleep(2)
                if self.is_stop:
                    print("Установлен стоппер")
                print("Processing...")
        except KeyboardInterrupt:
            self.stop()


    def stop(self):
        print('Начала отановки')
        self.listening = False
        self.processing = False

        """
        with open(r'C:\\Users\salim\PycharmProjects\Ella\speechList.txt', "w", encoding="utf-8") as f:
            f.write("")
        """
        while not self.speech_queue.empty():
            self.speech_queue.get()

        while not self.llm_queue.empty():
            self.llm_queue.get()



def main():
    print("Начало работы программы")
    assistant = AssistantSpeecher()
    assistant.start()


if __name__ == "__main__":
    main()
    """
    with open(r"C:\\Users\salim\PycharmProjects\Ella\speechList.txt", "r") as f:
        print(f.read())
    """







