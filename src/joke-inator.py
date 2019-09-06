# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import requests
from pprint import pprint
from guizero import App, TextBox
from time import localtime, time

timezone = -6 * (60*60) # UTC - 6:00

def main():
    global textBox, lastChanged
    joke = getJoke()
    lastChanged = 0
    print (joke['joke'])
    app = App(title="Joke-inator", width=500, height=100)
    textBox = TextBox(app, multiline=True, width=50, height=5)
    textBox.tk['wrap'] = 'word'
    
    textBox.value = joke['joke']
    textBox.enabled=False

    app.repeat(500, checkTime)
    app.display()

def updateJoke():
    global textBox
    joke = getJoke()
    textBox.enabled=True
    textBox.value = joke['joke']
    textBox.enabled=False
    print (joke['joke'])

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
