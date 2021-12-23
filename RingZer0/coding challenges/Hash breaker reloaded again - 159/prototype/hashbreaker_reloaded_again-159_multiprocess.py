#!/usr/bin/env python
#coding=utf-8
__author__ = 'M0nsieurPsych0'


import re
import requests
import bs4
import hashlib
import string
import random
import multiprocessing
import threading
import time
from os import urandom

'''
The challenge:
                You have 3 seconds to break this hash
                Send the answer back using https://ringzer0ctf.com/challenges/159/[clear_text]
'''
'''
The Writeup:
                As always the first step is defining the challenge boundaries.
                We know this hash is sha1 like the previous challenge so first thing I did was use hashcat to bruteforce a couple of hashes.
                **If you don't know hashcat, it's an amazing tool to bruteforce all sorts of hashes using CPU or GPU. It's amazing!**
                So the difference is that instead of having only numbers as input we also have lower case letters in the mix.
                The total amount of possibilities is now 36^6 = 2,176,782,336.
                What that means is that we can't generate a perfect hash in less than 3 seconds for all possibilities at least not with a regular CPU and only one thread.
                With a 1070ti and hashcat I am able to bruteforce a hash in less than a second. 
                The problem is that there is a warmup time before we start the process which in total time exceeds the 3 seconds allowed.

                My next idea was to generate a list of all possibilities, but I ran into a lot a problems. 
                First, I was using a text file with a hash:text for every line.
                The advantage of this is that I was only limited by the disk space, but the lookup is too slow for this challenge.
                In python a dictionnary lookup is a lot faster, but generating all of it in ram is too much, at least for my 128go server. 
                I was only able to generate about 16% of 36^6 which is more than a 100go of ram so this one was a no go as well.

                My next idea was to use the *power of probabilities*, in effect we don't need to generate all possibilities.
                In fact, we know that the probability of having the same value multiple times like "aaaaaa" is 6!(720) / 36^6 = 0.000033%.
                Even if we count the probability for all the letters 6!*36(25920) / 36^6 = 0.0011%.
                So the probability is lower than starting with any other random value

                  


'''

class hashbreaker_reloaded_again():
    def __init__(self):
        self._sha1_dict = {}
        self._charList = string.ascii_lowercase + string.digits
        self._tries = 0
        self._queue = multiprocessing.Queue()
        self._dictCap = 5000000
    
    
    def randomizer3000(self, maxsize):
        
        if random.randrange(0, 11) <= 5:
            andian = "little"
        else:
            andian = "big"
        
        return int.from_bytes(urandom(10), andian) % maxsize
    
    def createRandomSha1(self, q):

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
                q.put(self._sha1_dict)
                
    
    def pageRequests(self, q):
        payload = {'action': 'login', 'username': '*', 'password': '*'}

        with requests.session() as c:
            #we log in using the credential from payload
            c.post('https://ringzer0ctf.com/login', data=payload)
            lehash = None

            # we parse the page until the hash is in our list
            while lehash not in self._sha1_dict:
                self._sha1_dict = q.get()
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

        # Compute hash on a different subprocess
        # multiprocessing.Process(target=self.createRandomSha1, args=[self._queue],daemon=True).start()

        # query the progress and send request to get hash
        flag = self.pageRequests(self._queue)
        print(f"Found the flag in {len(self._sha1_dict)} generated sha1 hash and {self._tries} tries")     
        print("time elapse: ", time.perf_counter() - tz)
        print(flag)

if __name__ == "__main__":
    hashbreaker_reloaded_again().main()
