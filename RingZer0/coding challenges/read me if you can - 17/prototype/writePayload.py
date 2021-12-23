#!/usr/bin/env python
#coding=utf-8
__author__ = 'M0nsieurPsych0'

from base64 import b64decode

class WritePayload():
    def __init__(self):
        # self.payload = "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"
        self.payload = ""
    
    def _writePayload(self, filename, payload):
        # "Créer un nouveau fichier à partir du payload d'une string en base64"
        with open(f"{filename}", "wb") as copy:
            copy.write(b64decode(payload))

    def main(self):
        self._writePayload("test.png", self.payload)

if __name__ == "__main__":
    WritePayload().main()