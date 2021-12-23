
import bs4
import requests
import re
import hashlib

payload = {'action': 'login', 'username': '*', 'password': '*'}

with requests.session() as c:
    #we log in using the credential from payload
    c.post('https://ringzer0ctf.com/login', data=payload)

    #we parse the html code of the page to get the unconverted hash
    response = c.get('https://ringzer0ctf.com/challenges/13')
    html = bs4.BeautifulSoup(response.text, features="html5lib")
    tag = html.findAll("div",{"class":"message"})
    
    #we use regex to find everything between <br/> tags
    match = re.search(r'<br/>\n(.*)<br/>', str(tag[0]))
    lehash = match.group(1)

    #we hash to sha512
    lehash512 = hashlib.sha512(str.encode(lehash.strip())).hexdigest()

    #we concatenate the adress to send with our sha512 hash
    adresse = "https://ringzer0ctf.com/challenges/13/" + lehash512

    #we send the sha512 by getting the page 
    response = c.get(adresse)    

    #Overkill regex to find and isolate the flag from the get response
    flag = re.search(r'<div class="alert alert-info">(.*)</div>', str(response.text))

    #We print the flag
    print(flag.group(1))
    




