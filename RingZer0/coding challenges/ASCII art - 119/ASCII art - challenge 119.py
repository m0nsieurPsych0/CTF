import requests
import re
import bs4

def DetermineNumber(input):
      
    if (input == ' xxx x   xx   xx   x xxx '):
        return '0'

    if (input == ' xx  x x    x    x  xxxxx'):
        return '1'

    if (input == ' xxx x   x   xx  x   xxxxx' or input == ' xxx x   x   xx  x   xxxxx ' or input == ' xxx x   x   xx  x   xxxxx'):
        return '2'

    if (input == ' xxx x   x  xx x   x xxx' or input == ' xxx x   x  xx x   x xxx '):
        return '3'
    
    if (input == ' x   xx    x xxxxx     x    x'):
        return '4'

    if (input == 'xxxxxx     xxxx    xxxxxx'):
        return '5'


payload = {'action': 'login', 'username': '*', 'password': '*'}
challengeNumber = '119'

with requests.session() as c:
    #we log in using the credential from payload
    c.post('https://ringzer0ctf.com/login', data=payload)

    #we parse the html code of the page to get the unconverted hash
    response = c.get('https://ringzer0ctf.com/challenges/' + challengeNumber)
    html = bs4.BeautifulSoup(response.text, features="html5lib")
    tag = html.findAll("div",{"class":"message"})
    
    #we use regex to find everything between <br/> tags
    match = re.search(r'<br/>\n(.*)<br/>', str(tag[0]))
    
    #we isolate the numbers from the "begin" and "end" tags and we eliminate whitespace
    match2 = match.group(1).strip()
    
    #We split every element between the '<br/>' tag
    match2 = match2.split('<br/>')
    
    #Variables init
    j = 0
    combine = ''
    number = ''
    
    #We loop through the array of elements that we splitted
    for i in range(0, len(match2)):
        #If the element is not an empty string 
       if(match2[i] != ''):
           j += 1
           combine += match2[i]#We add the element to determine a line out of 5 that compose the number
           
           #When j equal 5 we have all the lines to determine the number
           if(j == 5):
               number += DetermineNumber(combine)#send to function and determine which numbers it is
               j = 0
               combine = ''

    
    #we concatenate the adress and the number
    adresse = "https://ringzer0ctf.com/challenges/" + challengeNumber + '/' + number
    
    #we send the answer by getting the page 
    response = c.get(adresse)    

    #Regex to find and isolate the flag from the get response
    flag = re.search(r'<div class="flag">(.*)</div>', str(response.text))

    #We print the flag
    print(flag.group(1))