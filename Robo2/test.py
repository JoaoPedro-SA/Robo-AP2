import pyautogui
import time
import subprocess

print("por favor não mecha no mouse ou teclado durante a execução do script")

# 1. Abre o navegador (Chrome)
subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
time.sleep(5)  # espera o Chrome abrir

# 2. Navega para o Gmail
pyautogui.write("https://mail.google.com")
pyautogui.press("enter")

time.sleep(5)  # espera carregar o Gmail (faça login manualmente se precisar)

# seta para esquerda
pyautogui.press("left")

# seta para cima
pyautogui.press("up")
time.sleep(5)
pyautogui.press("enter")
time.sleep(5)
pyautogui.write("antunesjoaopedro3@gmail.com")
time.sleep(5)
pyautogui.press("enter")
pyautogui.press("tab")
time.sleep(5)
pyautogui.write("Prova final")
pyautogui.press("tab")
time.sleep(5)
pyautogui.write("Olá, este é um teste de automação com PyAutoGUI.")
pyautogui.press("tab")
time.sleep(5)
pyautogui.press("enter")  # Envia o e-mail
#vanderson.bossi@faculdadeimpacta.com.br