#!/usr/bin/python3
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import requests
from pprint import pprint
from guizero import App, Text
from time import localtime, time, sleep
import datetime
import textwrap
import socket
import logging
import sys
import os

filename = os.path.basename("__file__")
logger = logging.getLogger("calendar-inator")
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s] %(message)s',
                     filename="/home/pi/mylogs.log")
logger.info("Program start.")
sys.stderr.write = logger.error
sys.stdout.write = logger.info


timezone = -6 * (60*60) # UTC - 6:00

def main():
    global textBox, lastChanged
    lastChanged = 0

    app = App(title="Joke-inator", width=500, height=100)
    app.tk.geometry('%dx%d+%d+%d' % (500, 100, 1400, 50))
    textBox = Text(app, size=14)

    updateJoke()

    app.repeat(500, checkTime)
    app.display()

def updateJoke():
    global textBox
    joke = getJoke()
    
    jokeText = joke['joke']
    jokeText = textwrap.wrap(jokeText,58)
    jokeText = '\n'.join(jokeText)
    textBox.value = jokeText

    now = datetime.datetime.now()    
    print(now.strftime("%Y-%m-%d %H:%M:%S")+" " + jokeText)

def getJoke():
    url = 'https://icanhazdadjoke.com'
    headers = {'User-agent':'joke-inator david@inators.net','Accept':'application/json'}
    r = requests.get(url, headers=headers, stream=True)
    
    joke = r.json()
    return joke

def checkTime():
    global lastChanged, timezone
    seconds = int(time())
    seconds += timezone
    if seconds % (60*60*12) == 0 and seconds > lastChanged : #every noon and midnight(ish)
        lastChanged = seconds
        updateJoke()

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Check for internet connectivity by trying to establish a socket connection.
    :param host: Host to connect to (default is Google's public DNS server).
    :param port: Port to connect to (default is 53, the DNS service port).
    :param timeout: Connection timeout in seconds.
    :return: True if the connection is successful, False otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.close()
        return True
    except socket.error:
        return False

def wait_for_internet_connection(interval=5):
    """
    Wait for an internet connection, checking periodically.
    :param interval: Time in seconds between checks.
    """
    print("Checking for internet connection...")
    while not check_internet_connection():
        print("No internet connection available. Waiting...")
        time.sleep(interval)
    print("Internet connection established.")

    


if __name__ == "__main__":
    try:
        wait_for_internet_connection()
        main()
    except Exception as e:
        logging.exception("Something happened")
