import requests
from hashlib import md5
from bs4 import BeautifulSoup

def merge(string1, string2):
    from itertools import zip_longest
    tuples = list(zip_longest(string1, string2, fillvalue=''))
    merged = "".join(str(i) + str(j) for i, j in tuples)
    return merged

IP = "switch ip"
URL = "http://" + IP + "/login.cgi"
password = "yourpassword"

page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')

rand = soup.find('input', {'id': 'rand'}).get('value')

merged = merge(password, rand)

print(md5(merged.encode()).hexdigest())
