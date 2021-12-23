import itertools
import hashlib
import string

'''def guess_password(real):
    #From string library, put all listable lowercase ascii + all digits 0-9 in a string
    chars = string.ascii_lowercase + string.digits 
    attempts = 0
    #For loop of the starting length of the password to max length
    for password_length in range(6, 7):
        #Use itertools, to iterate every char from "chars" with the length of password
        for guess in itertools.product(chars, repeat=password_length):
            attempts += 1#Calculate the number of attemps
            guess = ''.join(guess)#Concatenate each guess until password length is reached
            if guess == real:#If guess is the same as the password, WIN!
                return 'password is {}. found in {} guesses.'.format(guess, attempts)
            print(guess, attempts)'''


def generate_password_and_hash(f):
    #From string library, put all listable lowercase ascii + all digits 0-9 in a string
    chars = string.ascii_lowercase + string.digits 
    attempts = 0
    #For loop of the starting length of the password to max length
    for password_length in range(6, 7):
        #Use itertools, to iterate every char from "chars" with the length of password
        for guess in itertools.product(chars, repeat=password_length):
            attempts += 1#Calculate the number of attemps
            guess = ''.join(guess)#Concatenate each guess until password length is reached
            encodedguess = str(guess).encode('ascii')
            hashedguest = hashlib.sha1(encodedguess).hexdigest()
            f.write(hashedguest + ' ' + guess + '\n')

filename = "sha1ANDclear"

f = open(filename, 'w')

generate_password_and_hash(f)

f.close()

