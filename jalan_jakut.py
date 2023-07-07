#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import json
from bs4 import BeautifulSoup
import requests
import re

url = 'https://kodepos.id/jalan'
kode_post =["14320", "14340", "14330", "14350", "14360", "14310", "14370", "14470", "14460", "14450",
           "14440", "14430", "14420", "14410", "14210", "14270", "14230", "14260", "14240", "14250",
           "14120", "14110", "14150", "14140", "14130"] # daftar kode post jakarta utara
hasil_scraping = []

for kode in kode_post:
    url_= f"{url}/{kode}"
    response = requests.get(url_)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    #search elements needed by inspecting element on website
    try :
        #find page total
        page = soup.find('div', {"class" : "pagination"})
        detail = page.find_all('a')

        #find_table
        table = soup.find('table', {"class" : "table tablej"})
        rows = table.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            cols= [ele.text.strip() for ele in cols]
            hasil_scraping.append(cols)
            
        for i in range(len(detail)-2): #extracting data for the last 2 pages only (next page)
            next_page_link = soup.find('a', href=f'?page={i+2}')
            next_page_url = f"{url_}/?page={i+2}"
            next_response = requests.get(next_page_url)
            next_content = next_response.content
            next_soup = BeautifulSoup(next_content, 'html.parser')
            table2 = next_soup.find('table', {"class" : "table tablej"})
        try :
            rows2 = table2.find_all('tr')
        except :
            rows2 = [0]
        try :
            cols=""
            for row in rows2:
                cols = row.find_all('td')
                cols= [ele.text.strip() for ele in cols]
                hasil_scraping.append(cols)

        except :
            cols= None
            
    except Exception as e:
        print("Exception at", str(e))
             
df_hasil = pd.DataFrame(hasil_scraping)
df_hasil.columns= ['nama_jalan', 'kode_post']
df_hasil.dropna()
df_hasil = df_hasil.dropna()

alamat= []

for element in df_hasil["nama_jalan"]:
    jln = re.split(r'\bJln\. ', element)[-1].split(' - ')[0]
    kel = re.split(r'\bKel\. ', element)[-1].split(' - ')[0]
    kec = re.split(r'\bKec\. ', element)[-1].split(' - ')[0]
    kota = element.split(' - ')[-1]
    alamat_ = {"Jalan" : jln, "subDistrict" : kel, "district": kec, "city": kota}
    alamat.append(alamat_)

address =pd.DataFrame(alamat)
address['Jalan'] = address['Jalan'].apply(lambda x: f"Jalan {x}")
address.to_csv("jalan_jakut.csv")

#print(address)

