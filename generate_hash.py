import requests
from hashlib import md5
from bs4 import BeautifulSoup

def makeHash(IP, password):
    # Make a password hash, ip maynot contain anything else, so switch.local not https://switch.local
    URL = "http://" + IP + "/login.cgi"
    print(URL)
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    rand = soup.find('input', {'id': 'rand'}).get('value')
    merged = merge(password, rand)
    print(md5(merged.encode()).hexdigest())
    return(md5(merged.encode()).hexdigest())

def merge(string1, string2):
    from itertools import zip_longest
    tuples = list(zip_longest(string1, string2, fillvalue=''))
    merged = "".join(str(i) + str(j) for i, j in tuples)
    return merged

