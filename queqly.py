import asyncio
import tkinter as tk
from tkinter import ttk
import threading

class AsyncTkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Асинхронный ИИ-агент")
        self.root.geometry("400x300")

        # Интерфейс
        self.label = ttk.Label(root, text="Готов к работе", font=("Arial", 14))
        self.label.pack(pady=20)

        self.start_btn = ttk.Button(root, text="Запустить агента", command=self.start_agent)
        self.start_btn.pack(pady=10)

        self.stop_btn = ttk.Button(root, text="Остановить", command=self.stop_agent, state="disabled")
        self.stop_btn.pack(pady=10)

        # Переменные
        self.running = False
        self.agent_task = None

        # Получаем asyncio event loop
        self.loop = asyncio.new_event_loop()

    def start_agent(self):
        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.label.config(text="Агент запущен...")

        # Запускаем асинхронную задачу в отдельном потоке
        thread = threading.Thread(target=self.run_async_agent, daemon=True)
        thread.start()

    def run_async_agent(self):
        """Запускает асинхронную задачу в отдельном потоке"""
        asyncio.set_event_loop(self.loop)
        self.agent_task = self.loop.create_task(self.agent_loop())
        self.loop.run_until_complete(self.agent_task)

    async def agent_loop(self):
        """Основной цикл агента"""
        i = 0
        while self.running:
            self.label.config(text=f"Агент работает... Цикл {i}")
            await asyncio.sleep(1)  # имитация анализа скриншота
            i += 1
            # Здесь мог бы быть:
            # - Скриншот экрана
            # - Запрос к LLM
            # - Выполнение действия
        self.label.config(text="Агент остановлен")

    def stop_agent(self):
        self.running = False
        if self.agent_task:
            self.agent_task.cancel()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    def close(self):
        self.running = False
        if self.agent_task:
            self.agent_task.cancel()
        self.root.quit()


# === Запуск приложения ===
if __name__ == "__main__":
    root = tk.Tk()
    app = AsyncTkApp(root)

    # Обработка закрытия окна
    root.protocol("WM_DELETE_WINDOW", app.close)

    # Запускаем Tkinter mainloop
    root.mainloop()