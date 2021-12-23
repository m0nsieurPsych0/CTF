#!/usr/bin/env python
#coding=utf-8
__author__ = 'm0nsieurPsych0'

import subprocess
import re

'''
    The challenge:
                    Connecting to a remote server using SSH and solving a sudoku puzzle.
                    Ex:
                        The sudoku challenge

                    +---+---+---+---+---+---+---+---+---+
                    |   |   |   |   | 8 |   |   | 6 | 4 |
                    +---+---+---+---+---+---+---+---+---+
                    |   |   |   |   | 6 |   |   |   |   |
                    +---+---+---+---+---+---+---+---+---+
                    | 4 |   |   | 5 |   |   |   |   |   |
                    +---+---+---+---+---+---+---+---+---+
                    |   | 4 |   | 8 |   |   | 3 |   | 6 |
                    +---+---+---+---+---+---+---+---+---+
                    |   |   |   | 2 |   |   |   |   |   |
                    +---+---+---+---+---+---+---+---+---+
                    | 8 |   | 7 | 4 |   |   | 2 |   |   |
                    +---+---+---+---+---+---+---+---+---+
                    | 6 |   |   |   |   |   |   | 7 | 3 |
                    +---+---+---+---+---+---+---+---+---+
                    |   |   |   |   | 2 |   | 6 |   |   |
                    +---+---+---+---+---+---+---+---+---+
                    | 1 |   | 5 | 6 |   | 8 |   |   |   |
                    +---+---+---+---+---+---+---+---+---+

                    Solve this sudoku in less than 10 seconds and you'll get the flag.

                    Submit all the sudoku table using this format from left to right 1,2,3,4,5,6,7,8,9,2,3,4,5,6,7,8,9,1...
'''
'''
    The writeUp:
                First thing to do is be able to control an interactive SSH session.
                I want to try to use pipes to communicate with subprocesses.
                For the first part I want to be able to login automatically:
                ssh is special, it doesn't want user to just pass in a password using for exemple "echo 'password\n' | ssh sudoku@challenges.ringzer0team.com -p 10143"
                I could use something like sshPass, but then I will not be able to interact with the shell to send the solved sudoku.


'''

class Classic_sudoku_143():
    def __init__(self):
        # self._ssh = "ssh sudoku@challenges.ringzer0team.com -p 10143"
        self._ssh = ["ssh", "-T" ,"sudoku@challenges.ringzer0team.com", "-p",  "10143"]
        self._password = "dg43zz6R0E\n"

    def parsingSudoku(self):
        pass

    def solvingSudoku(self):
        pass

    def sshSession(self):
        pass

    def main(self):
        # with subprocess.Popen(self._ssh, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as ssh:
        with subprocess.Popen(self._ssh, shell=False, stdin=subprocess.PIPE) as ssh:
            # result = ssh.stdout.readlines()
            # if result == []:
            #     print(ssh.stderr.readlines())
            # elif result == "sudoku@challenges.ringzer0team.com's password: ":
            result = ssh.communicate(input=self._password.encode())
            print(result)
        
        # print(result)

if __name__ == "__main__":
    Classic_sudoku_143().main()