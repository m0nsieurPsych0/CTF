import requests
import re
import hashlib
import bs4


payload = {'action': 'login', 'username': '*', 'password': '*'}

with requests.session() as c:
    #we log in using the credential from payload
    c.post('https://ringzer0ctf.com/login', data=payload)

    #we parse the html code of the page to get the unconverted hash
    response = c.get('https://ringzer0ctf.com/challenges/56')
    html = bs4.BeautifulSoup(response.text, features="html5lib")
    tag = html.findAll("div",{"class":"message"})
    
    #we use regex to find everything between <br/> tags
    match = re.search(r'<br/>\n(.*)<br/>', str(tag[0]))
    lehash = match.group(1).strip()
   
    #We know the hash is a value from 0 to 9999
    #Generate sha1 hash from a value from 0 to 9999
    for value in range(0, 10000):
        bytevalue = str(value).encode('ascii')
        hashed = hashlib.sha1(bytevalue).hexdigest()
        
        #We compare the parsed hash with the one we generated
        if (lehash == hashed):#if true we send the clear text answer

            #we strip the string of the bytevalue interpretation from "b' '"
            answer = str(bytevalue).strip('b').strip(r"'")
            #we concatenate the adress to send with our clear text unhashed answer
            adresse = "https://ringzer0ctf.com/challenges/56/" + answer

            #we send the clear text unhashed answer by getting the page 
            response = c.get(adresse)

            #Overkill regex to find and isolate the flag from the get response
            flag = re.search(r'<div class="alert alert-info">(.*)</div>', str(response.text))

            #We print the flag
            print(flag.group(1))
             
