import speech_recognition as sr
import pyttsx3
import queue
import threading
import requests
import time
from llm import llm_response
import re


class AssistantSpeecher():
    def __init__(self):
        self.listening = False
        self.processing = False



        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()


        self.speech_queue = queue.Queue()
        self.llm_queue = queue.Queue()


    def setup_microphone(self):
        try:
            print("Настройка микрофона")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print("Возникла ошибка при настройке микрофона"); print(e)


    def setup_tts_engine(self):
        self.tts_engine = pyttsx3.init()

        self.tts_engine.startLoop(False)

        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.8)


    def speech_recognizer(self):
        print("Прослушивание начилось")
        while self.listening:
            try:
                with self.microphone as source:
                    print("Вот сейчас точно идет прослушивание")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)

                def regognize():
                    try:
                        print("Распознавание началось")
                        text = self.recognizer.recognize_google(
                            audio,
                            language="ru-RU"
                        )

                        if any( step_word in text.lower() for step_word in ["стоп","остановись","остановка", "не продолжай"]):
                            print("Обнаружено стоп-слово")
                            if self.tts_engine.isBusy():
                                self.tts_engine.stop()

                        if len(text.strip())>3:
                            print("Текст добавлен в очередь")
                            self.speech_queue.put(text)

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
                    request = requests.get("https://www.google.com").content[:20]
                    #request = llm_response(str(text))
                    if request:
                         self.llm_queue.put(request)
            except queue.Empty:
                continue
            except Exception as e:
                print("Ошибка в точке 33")
                print(e)
                time.sleep(0.1)

    def tts_loop(self):
        while self.tts_engine.isBusy():
            self.tts_engine.iterate()
            time.sleep(0.05)


    def tts_say(self):
        while self.processing:
            try:
                text = self.llm_queue.get(timeout=1)
                if text:
                    print("text generate")
                    print("Вот мой текст === " + str(text))
                    self.speak(text)
                    time.sleep(0.5)
            except queue.Empty:
                continue
            except Exception as e:
                print("Ошибка в точке 45")
                print(e)
                time.sleep(0.1)

    def speak(self, text):
        try:
            if not self.tts_engine.isBusy():
                self.setup_tts_engine()
                self.tts_engine.say(text)
                self.tts_loop()
            else:
                self.tts_engine.endLoop()
                self.tts_engine.stop()

                while not self.speech_queue.empty():
                    self.speech_queue.get()

                while not self.llm_queue.empty():
                    self.llm_queue.get()


        except Exception as e:
            print("Возникла ошибкав точке 56")
            print(e)

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
                time.sleep(0.1)
                if int(time.time())%10 == 0:
                    print(f"Временной индикатор - {int(time.time())}")
                    print(f"Размер очереди распознаной речи - {self.speech_queue.qsize()}")
                    print(f"Размер очереди озвучиваемой речи - {self.llm_queue.qsize()}")
        except KeyboardInterrupt:
            self.stop()

        for i in threadings:
            i.join()


    def stop(self):
        print('Начала отановки')
        self.listening = False
        self.processing = False


        while not self.speech_queue.empty():
            self.speech_queue.get()

        while not self.llm_queue.empty():
            self.llm_queue.get()

        time.sleep(1)
        self.tts_engine.endLoop()
        print("Программа остановлена")




def main():
    print("Начало работы программы")
    assistant = AssistantSpeecher()
    assistant.start()


if __name__ == "__main__":
    main()








