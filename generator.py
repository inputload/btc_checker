import subprocess
import sys
import requests


def create():
    with open("dict/english_alpha.txt", 'r') as rus:
        file = rus.read().split("\n")
    for i in file:
        subprocess.Popen([sys.executable, 'check.py', i])
    response = requests.post(
        url='https://api.telegram.org/bot1420550733:AAGv9VhgYDyA1cJr76Mt-ToEdnk6s59poFg/sendMessage',
        data={'chat_id': 1293582406, 'text': 'Словарь кончился'}
    ).json()


create()
