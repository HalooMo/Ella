import pyttsx3
import threading
import time


class SpeakUP():
    def __init__(self):
        self.count = 0
        self.is_stop = False
        self.time_satrt = 0 #Надо установить при запуске
        self.processing = False
        self.speak_stop_event = threading.Event()




    def tts_loop(self,):
        while self.processing:
            try:
                if self.speak_stop_event.is_set() and not self.is_stop:
                    continue
                while self.tts_engine.isBusy():
                    self.tts_engine.iterate()

                    time.sleep(1)
            except Exception as e:
                print(e)



    def tts_controller(self):
        while self.processing:
            if self.speak_stop_event.is_set() and not self.is_stop:
                self.restart_tts_engine()
            else:
                delta_time  = self.time_counter()
                if delta_time % 10 == 0 and self.time_start != int(time.time()):
                    self.speak()
                    time.sleep(0.5)


    def stopper_thread(self):
        while self.processing:
            delta_time = self.time_counter()
            if delta_time % 11 == 0 and self.time_start != int(time.time()):
                time.sleep(0.5)
                self.speak_stop_event.set()



    def start(self):
        self.processing = True
        self.time_start = int(time.time())
        self.setupt_tts_engine()
        self.threadings = []

        self.threadings.append(threading.Thread(target=self.tts_loop, daemon=True))
        self.threadings.append(threading.Thread(target=self.tts_controller, daemon=True))
        self.threadings.append(threading.Thread(target=self.stopper_thread, daemon=True))

        for i in self.threadings:
            i.start()

    def speak(self):
        self.tts_engine.say(f"Someting i say, it is no  matter, something yet - здесь написанно что я что -то типо как-то говорю в  {self.count} раз ")
        self.count += 1

    def setupt_tts_engine(self,):
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 1.0)
        self.tts_engine.startLoop(False)

    def time_counter(self):
        return int(time.time()) - self.time_start

    def restart_tts_engine(self,):
        self.is_stop = True
        print("Остановка движка...")
        self.tts_engine.stop()
        self.tts_engine.endLoop()
        print("Движок остановлен!")
        self.setupt_tts_engine()
        print("Начало перезапуска движка")
        time.sleep(0.5)
        print("Конец перезапуска движка")
        self.speak_stop_event.clear()
        self.is_stop = False

def main():
    speaker = SpeakUP()
    speaker.start()
    while speaker.processing:
        print("Выполнение программы...")
        time.sleep(3)


if __name__ == "__main__":
    main()










