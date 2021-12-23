#!/usr/bin/env python
#coding=utf-8
__author__ = 'M0nsieurPsych0'


import re
import requests
import bs4
import hashlib
import string
import random
import threading
import time
from os import urandom



class hashbreaker_reloaded_again():
    def __init__(self):
        self._sha1_dict = {}
        self._charList = string.ascii_lowercase + string.digits
        self._tries = 0
        self._dictCap = 5000000
    
    
    def randomizer3000(self, maxsize):
        
        if random.randrange(0, 11) <= 5:
            andian = "little"
        else:
            andian = "big"
        
        return int.from_bytes(urandom(10), andian) % maxsize
    
    def createRandomSha1(self):

        while len(self._sha1_dict) < self._dictCap:
            # We create a guess of 6 char
            guess = str()
            while(len(guess) < 6):
                # we pick at random (one of 36 choices)
                randChar = self._charList[self.randomizer3000(len(self._charList))]
                # Concatenate each guess until password length is reached
                guess += randChar
            
            encodedguess = str(guess).encode('ascii')
            hashedguess = hashlib.sha1(encodedguess).hexdigest()

            if hashedguess not in self._sha1_dict:
                self._sha1_dict[hashedguess] = guess
                
    
    def pageRequests(self):
        payload = {'action': 'login', 'username': '*', 'password': '*'}

        with requests.session() as c:
            #we log in using the credential from payload
            c.post('https://ringzer0ctf.com/login', data=payload)
            lehash = None

            # we parse the page until the hash is in our list
            while lehash not in self._sha1_dict:
                response = c.get('https://ringzer0ctf.com/challenges/159')
                
                html = bs4.BeautifulSoup(response.text, features="html5lib")
                tag = html.findAll("div",{"class":"message"})
                
                #we a regex to find everything between <br/> tags
                match = re.search(r'<br/>\n(.*)<br/>', str(tag[0]))
                lehash = match.group(1).strip()
                print(lehash)
                self._tries += 1
                    
            answer = self._sha1_dict[lehash]
            # we concatenate the adress to send with our clear text unhashed answer
            address = "https://ringzer0ctf.com/challenges/159/" + answer
            # we send the clear text answer
            response = c.get(address)
            # find the flag
            flag = re.search(r'<div class="alert alert-info">(.*)</div>', str(response.text))
            # We return the flag
            return flag.group(1)

    def main(self):
        threading.Thread(target=self.createRandomSha1, daemon=True).start()
        
        # timer
        tz = time.perf_counter()

        # query the progress and send request to get hash
        flag = self.pageRequests()
        print(f"Found the flag in {len(self._sha1_dict)} generated sha1 hash and {self._tries} tries")     
        print("time elapse: ", time.perf_counter() - tz)
        print(flag)

if __name__ == "__main__":
    hashbreaker_reloaded_again().main()
