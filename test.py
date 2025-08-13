import pyautogui
import subprocess
import time

# abrir bloco de notas
subprocess.Popen("notepad.exe")
time.sleep(1)

# Escrever algo
pyautogui.typewrite("Oi! Eu sou um teste.", interval=0.1)

#fechar bloco de notas
pyautogui.hotkey("alt", "f4")