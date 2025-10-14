import pyautogui
import time

# Открыть меню "Пуск" (Win + R)
pyautogui.hotkey('win', 'r')
time.sleep(0.5)

# Ввести команду для открытия браузера
pyautogui.write('chrome https://www.google.com?q=hotels')
time.sleep(1)
pyautogui.press('enter')

time.sleep(3)  # Подождать загрузки
pyautogui.write('погода сегодня', interval=0.2)
pyautogui.press('enter')