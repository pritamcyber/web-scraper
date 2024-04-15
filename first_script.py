from bs4 import BeautifulSoup
import requests
from pathlib import Path
import pandas as pd

# write here your file name 
links = pd.read_excel("web_scraping\data.xlsx",header=None,names = ['A'])
print(links.iloc[0])

all_links = []
all_images = []
all_para = []
all_text = []
whole_text = []
print(links.shape)


# this method finds all the Image links in any given Webpage  
def image_finder(soup,li):
    s =  str(li)
    ll = 'https://'
    com = str(s[0:int(str(s[8:]).find('/'))+len(ll)]).strip()
    img_tags=soup.find_all('img')
   
    for i  in img_tags:
        try:
            if i.has_attr('data-src'):                
                
                if not str(i['data-src']).startswith('https:/') and not str(i['data-src']).startswith('http:/') :
                    value = com+str(i['data-src']).strip()
                    all_links.append(value)
                else:
                    all_images.append(str(i['data-src']))
                    
            elif i.has_attr('src'):
                
                if not str(i['src']).startswith('https:/') and not str(i['src']).startswith('http:/') :
                    value = com+str(i['src']).strip()
                    all_links.append(value)
                else:
                    all_images.append(str(i['src']))
        
            elif i.has_attr('data-lsrc'):
                
                if not str(i['data-lsrc']).startswith('https:/') and not str(i['data-lsrc']).startswith('http:/') :
                    value = com+str(i['data-lsrc']).strip()
                    all_links.append(value)
                else:
                    all_images.append(str(i['data-lsrc']))
            else:
                print(i)
        except requests.exceptions.ConnectionError:
            response = requests.get(li)
            soup = BeautifulSoup(response.text,'html.parser')
    
   



#  this methods finds any  all paragraph from any given webpage which i thinks containes most of the informations
def para_text(soup):
        p = soup.find_all('p')
        
        for i in p:
            for x in i.stripped_strings:
                
                all_para.append(x)
                


# this methods reads all the text which body containes 
def full_body_text(soup,li):
    a=soup.find('body')

    try:
        
        for i in a.stripped_strings:
            whole_text.append(i) 
    except:
        pass


# this method finds all the links which containes in any webpage 
def link_founder(soup,li):
    a_tags = soup.find_all('a')
    s =  str(li)
    ll = 'https://'
    com = str(s[0:int(str(s[8:]).find('/'))+len(ll)]).strip()
    for  i in a_tags:
        try:
            if i.has_attr('href') and not str(i['href']).startswith("#"):
                if not str(i['href']).startswith('https:/') and not str(i['href']).startswith('http:/') :
                    value = com+str(i['href']).strip()
                    all_links.append(value)
                else:
                    all_links.append(str(i['href']))
            else:
                # print(i)
                pass
        except requests.exceptions.ConnectionError:
            response = requests.get(li)
            soup = BeautifulSoup(response.text,'html.parser')
count = 0




for i in range(0,links.shape[0]):
    print(i)
    ll = str(links.iloc[i][0])+'.csv'
    print(ll)
    
    try:        
        print(links.iloc[i][0])
        response = requests.get(links.iloc[i][0])
        soup = BeautifulSoup(response.text,'html.parser')
        
        count += 1
    except:
        print('this is error')
         
    image_finder(soup,links.iloc[i][0])
    link_founder(soup,links.iloc[i][0])
    para_text(soup)
    full_body_text(soup,links.iloc[i][0])

    link = all_links.copy()
    image = all_images.copy()
    scr = all_para.copy()
    body_text = whole_text.copy()
    
    all_images.clear()
    all_links.clear()
    all_para.clear()
    whole_text.clear()
    
    

    df1 = pd.DataFrame({'link':link})
    df2 = pd.DataFrame({'Image':image})
    df4 = pd.DataFrame({'Body_text':body_text})
    df3 = pd.DataFrame({'Text':scr})
    

    output_file = f'file{count}'+'.csv'
    output_file_path = Path(output_file)

    output_file_path.parent.mkdir(parents=True, exist_ok=True)
   

    pd.concat([df1,df2,df4,df3],axis=1).to_csv(output_file_path, index = False)
        










