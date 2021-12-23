#!/usr/bin/env python
#coding=utf-8

__author__ = 'M0nsieurPsych0'

import re
import requests
import bs4
import selenium
import time
import PIL

import easyocr
from base64 import b64decode, b64encode

'''
The challenge:
                You have 2 seconds to parse the word.
                Send the answer back using https://ringzer0ctf.com/challenges/17/[your_string]

                An image is shown with white letters on a mixed background
'''
'''
The writeup:
                First I thought, it might not be an OCR challenge.
                We have a payload in base64, maybe we can check the content and find what makes the white text.
                Otherwise this is an OCR challenge and we can use easyOCR or pytessaract.

                After comparing the bytes of the two images, there is too much difference between the two. 
                So this is a OCR challenge after all.

                Between pytessaract and easyOCR, I suggest using easyOCR. The installation process is a lot simpler.
                And reading other Writeup my interpretation is correct.

                Only detail to consider is to download 2 recognition models by running this command:
                
                ' reader = easyocr.Reader(['en','fr'], recog_network = 'latin_g1', gpu = False) '
                
                BEFORE you query the page for the challenge.

                Then for the rest we don't need to preprocess the image at all, we just decode the base 64 and feed the raw byte to easyOCR
                and VOILÀ!

                We need between 1 and 5 tries to get the flag, not bad at all! 
'''

class Read_me_if_you_can_17():
    def __init__(self):
        self._baseURL = "https://ringzer0ctf.com/challenges/"
        self._challengeNumber = "17"
        self._username = "*"
        self._password = "*"
    
    def _initOCR(self):
        # need to init this first       
        return easyocr.Reader(['en','fr'], recog_network = 'latin_g1', gpu = False, verbose=False)


    def _OCR(self, ocr, b64Payload):
        # reading text and returning the result
        return ocr.readtext(b64decode(b64Payload))[0][1]
    
    def _writeFlag(self, flag):
        with open("flag.txt", "w", encoding="utf-8") as f:
            f.write(flag)

    def _pageRequests(self):
        payload = {'action': 'login', 'username': self._username, 'password': self._password}
        ocr = self._initOCR()
        # Start the timer        
        tz = time.perf_counter()
        with requests.session() as c:
            # login using our credentials
            c.post('https://ringzer0ctf.com/login', data=payload)

            # we parse the page
            response = c.get(f"{self._baseURL}{self._challengeNumber}")
            
            html = bs4.BeautifulSoup(response.text, features="html5lib")
            tag = html.findAll("div",{"class":"message"})
                
            # we use a regex to catch everything between <br/> tags
            b64Payload = re.search(r'(<img src="data:image\/png;base64,)(.*)"/>', str(tag[0])).group(2).strip()
            
            # calling the ocr function on the payload
            answer = self._OCR(ocr, b64Payload)
            
            print(answer)

            # we send the clear text answer
            response = c.get(f"{self._baseURL}{self._challengeNumber}/{answer}")
            # find the flag
            flag = re.search(r'<div class="alert alert-info">(.*)</div>', str(response.text))
            # We return the flag
            try:
                return tz, flag.group(1)
            except AttributeError:
                # if there is no group for the flag variable we failed
                return tz, None
    
    def main(self):
        flag = None
        
        # Start the process
        while flag is None:
            # Sleep 5 seconds on fail
            time.sleep(5)
            
            tz, flag = self._pageRequests()
        
        print(f"time elapse: {time.perf_counter() - tz}")

        # Print stats and flag
        print(flag)

        # Write flag to file
        self._writeFlag(flag)

if __name__ == "__main__":
    Read_me_if_you_can_17().main()