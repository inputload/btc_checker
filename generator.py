import subprocess
import sys
import requests


def create():
    with open("dict/english_alpha.txt", 'r') as rus:
        file = rus.read().split("\n")
    index = 0
    for i in file:
        index += 1
        subprocess.Popen([sys.executable, 'check.py', i])
        if index // 1000 == 0:
            response = requests.post(
                url='https://api.telegram.org/bot1420550733:AAGv9VhgYDyA1cJr76Mt-ToEdnk6s59poFg/sendMessage',
                data={'chat_id': 1293582406, 'text': '1000 прошло'}
            ).json()
    response = requests.post(
        url='https://api.telegram.org/bot1420550733:AAGv9VhgYDyA1cJr76Mt-ToEdnk6s59poFg/sendMessage',
        data={'chat_id': 1293582406, 'text': 'Словарь кончился'}
    ).json()


create()
