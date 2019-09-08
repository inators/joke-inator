# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import requests
from pprint import pprint
from guizero import App, Text
from time import localtime, time
import datetime
import textwrap

timezone = -6 * (60*60) # UTC - 6:00

def main():
    global textBox, lastChanged
    lastChanged = 0

    app = App(title="Joke-inator", width=500, height=100)
    textBox = Text(app, size=14)

    updateJoke()

    app.repeat(500, checkTime)
    app.display()

def updateJoke():
    global textBox
    joke = getJoke()
    
    jokeText = joke['joke']
    jokeText = textwrap.wrap(jokeText,60)
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
    


if __name__ == "__main__":
    main()
