from bs4 import BeautifulSoup
import requests


links = 'https://products.basf.com/global/en/ci/n-vinyl-2-pyrrolidone.html'
response = requests.get(links)
soup = BeautifulSoup(response.text,'html.parser')
print(response)


a=soup.find('body')
soup.a.stripped_strings
# print(a)

for i in a.stripped_strings:
    print(i)