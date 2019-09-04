# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import requests
from pprint import pprint

def main():
    url = 'https://icanhazdadjoke.com'
    headers = {'User-agent':'joke-inator david@inators.net','Accept':'application/json'}
    r = requests.get(url, headers=headers, stream=True)
    
    joke = r.json()
    
    print (joke['joke'])



if __name__ == "__main__":
    main()
