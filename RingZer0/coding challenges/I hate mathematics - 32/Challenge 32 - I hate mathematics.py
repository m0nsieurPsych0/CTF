import re
import requests
#import hashlib


payload = {'action': 'login', 'username': '*', 'password': '*'}

with requests.session() as c:
    #we log in using the credential from payload
    c.post('https://ringzer0ctf.com/login', data=payload)

    #we parse the html code of the page to get the unconverted hash
    response = c.get('https://ringzer0ctf.com/challenges/32')
    #html = bs4.BeautifulSoup(response.text, features="html5lib")
    #tag = html.findAll("div",{"class":"message"})
    
    #we use regex to find everything between <br/> tags
    match = re.search(r'<br/>\n(.*)<br/>', str(response.text))
    lehash = match.group(1).strip()
    print(lehash)
    

    #extract the string
    string = r'7853 + 0x19bf - 10000000001110 = ?'
    #Strip whitespace left and right
    string = string.strip()
    #Split the string with each element
    string = string.split(' ')
    #Isolate each element to int
    decimal = string[0]
    decimal = int(decimal)
    hexa = string[2].strip('0x')
    hexa = int(hexa, 16) #int interpreted as hexadecimal
    binary = string[4]
    binary = int(binary, 2) #int interpreted as binary


    print(decimal)
    print('\n')
    print(hexa)
    print('\n')
    print(binary)
    summation = decimal + hexa - binary
    print('\n')
    print(summation)

    #we concatenate the adress to send with our sha512 hash
    #adresse = "https://ringzer0ctf.com/challenges/32/" + summation

    #we send the sha512 by getting the page 
    #response = c.get(adresse)    

    #Overkill regex to find and isolate the flag from the get response
    #flag = re.search(r'<div class="alert alert-info">(.*)</div>', str(response.text))


    #We print the flag
    #print(response.text)