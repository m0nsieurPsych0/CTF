#!/usr/bin/env python
#coding=utf-8
__author__ = 'M0nsieurPsych0'


class Compute():
    def __init__(self):
        self.i = 931
        self.j = 2800

    def formatValues(self, val1, val2, val3):
        # result = f"FLAG-DFEB0D{val2}-{val1}FDBECDF39D{val1}"
        result = f"FLAG-DFEB0D{val1}-{val2}FDBECDF39D{val2}"
        return result
    # previous flag 
    # FLAG-B493801CDB-831ABDDFA628AC31
    # FLAG-DFEB0D2829-720FDBECDF39D720 -> wrong flag
    # FLAG-DFEB0D2829-727FDBECDF39D727 -> wrong flag
    # FLAG-DFEB0D720-2829FDBECDF39D2829 -> wrong flag
    def main(self):
        # equation
        # I=931
        # J=2800
        #      11char           1char'-' 10char
        # FORMAT(11H FLAG-DFEB0D,I4,1H-,I3,10H FDBECDF39D,I3)
        # WRITE(6,1337)J+29,(J/4)+20,I
        val1 = self.j + 29
        # val2 = int((val1/4)+20)
        val2 = int((self.j/4)+20)
        val3 = self.i
        print(self.formatValues(val1, val2, val3))

if __name__ == "__main__":
    Compute().main()
