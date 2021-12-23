import requests
import re
import bs4

def AnagramSolver(word):
       response = c.get('https://anagram-solver.net/'+ word)
       verifiedWord = re.search(r'">(.*)</a></li>', str(response.text))
       return verifiedWord.group(1)

def CheckDictionary(word):
    f = open('english7letters.txt', 'r')
    found = False
    for line in f:
        if(word == line.strip('\n')):
             found = True
             return found
    return found
            
         
payload = {'action': 'login', 'username': '*', 'password': '*'}
challengeNumber = '126'

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
    match2 = match2.split(',')
    print(match2)
    answer = ''
        
    for word in match2:
        if(CheckDictionary(word) == False):
            answer += AnagramSolver(word)
        else:
            answer += word 
        
        if (word != match2[-1]):
                answer += ','

    print(answer)

    #we concatenate the adress and the number
    adresse = "https://ringzer0ctf.com/challenges/" + challengeNumber + '/' + answer
    
    #we send the answer by getting the page 
    response = c.get(adresse)
    #print(response.text)    

    #Regex to find and isolate the flag from the get response
    flag = re.search(r'<div class="alert alert-info">(.*)</div>', str(response.text))

    #Check if flag is present
    if (flag):#If the list is empty return to false
        print('too slow, try again')
    else:
    #We print the flag
        print(flag.group(1))