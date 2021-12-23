#!/usr/bin/env python
#coding=utf-8

__author__ = 'M0nsieurPsych0'

import re
import requests
import bs4
import time
from base64 import b64decode, b64encode
from itertools import cycle

'''
The challenge:

                You have 3 seconds decrypt this message using the xoring key
                hidden into the xor key string. 
                The length of the key is 10 characters.
                The message is encoded using base 64.
                Send the answer back using https://ringzer0ctf.com/challenges/16/[your_string]
'''
'''
The writeup:
                The first step is always to define the bondaries of the challenge so heres what I gathered:

                - we know the length of the key is variable
                - we know the key cannot be a permutation of all possibilities (aka factorial) otherwise the challenge would be a game of luck
                - we need to find 10 chars in the key that will be used to decrypts the message
                - the only thing left to do is to check every series of 10 chars in the given key

                After looking through the results I could not find which one was the correct one and started to doubt the xoring process.
                I even though that the key might be obfuscated in some way, maybe reversing it, rot13?
                After a while I finally gave up and I bought a hint.
                The hint says that we have to look for a key with only printable characters. 
                Of course! I had notice that one of them was all printable characters, but as I often do, I thought it could not be that...easy?
                
                Well I was wrong! The main reason is that we need to send the result as a get request in the url,
                so unprintable characters means we can't send as a printable string. 
                Of course, there is ways to encode the url but that's not the point of the challenge. 

                The rest is business as usual, setting up the parsing of the page and sending the result, 
                but if you got this far you already know how to do this, right? ;)
'''

class hashbreaker_reloaded_again():
    def __init__(self):
        self._baseURL = "https://ringzer0ctf.com/challenges/"
        self._challengeNumber = "16"
        self._username = "YourOwnUsername"
        self._password = "yourOwnPassword"
    
    # went too far...
    def _reverse(self, key):
        return key[::-1]
    
    def _writeFlag(self, flag):
        with open("flag.txt", "w", encoding="utf-8") as f:
            f.write(flag)

    # we can decode AND encode in case we need this in the future
    def _xoring(self, key, message, encode=False, decode=False):        
        if decode:
            message = b64decode(message).decode()
        
        xored = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(message, cycle(key)))
        
        if encode:
            return b64encode(xored.encode()).strip()

        return xored

    # this is the most important function to test series of 10 chars as a XOR key
    def _testKey(self, key, message):
        myRange = 10
        for i in range(0, len(key)):
            if i + myRange <= len(key):
                # using string splicing
                currentKey = key[i:i+myRange]
                result = self._xoring(currentKey, message, decode=True)
            else:
            # wrap around (not sure if this was needed, but it doesn't add too much computation so might as well be thorough)
                offset = len(key) - i
                currentKey = key[i: i + offset] + key[:myRange - offset]
                result = self._xoring(currentKey, message, decode=True)

            # Had to buy a hint on this one
            # The only way we know this is the correct key is to check that the string is only printable characters
            if result.isprintable():
                return result
    
    def _pageRequests(self):
        payload = {'action': 'login', 'username': self._username, 'password': self._password}

        with requests.session() as c:
            # login using our credentials
            c.post('https://ringzer0ctf.com/login', data=payload)
            
            matches = []
            key = None
            message = None

            # we parse the page
            response = c.get(f"{self._baseURL}{self._challengeNumber}")
            
            html = bs4.BeautifulSoup(response.text, features="html5lib")
            tag = html.findAll("div",{"class":"message"})
                
            # we use a regex to catch everything between <br/> tags
            for hit in tag:
               matches.append(re.search(r'<br/>\n(.*)<br/>', str(hit)).group(1).strip())
            
            key = matches[0]
            message = matches[1]

            answer = self._testKey(key, message)  
                    
            # we send the clear text answer
            response = c.get(f"{self._baseURL}{self._challengeNumber}/{answer}")
            # find the flag
            flag = re.search(r'<div class="alert alert-info">(.*)</div>', str(response.text))
            # We return the flag
            return flag.group(1)
    
    def main(self):
        # Start the timer        
        tz = time.perf_counter()
        
        # Start the process
        flag = self._pageRequests()

        # Print stats and flag
        print(f"time elapse: {time.perf_counter() - tz}")
        print(flag)

        # Write flag to file
        self._writeFlag(flag)

if __name__ == "__main__":
    hashbreaker_reloaded_again().main()