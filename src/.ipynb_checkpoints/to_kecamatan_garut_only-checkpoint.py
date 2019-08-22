import pandas as pd
import matplotlib.pyplot as plt
import requests
import lxml.html as lh
import pandas as pd
from urllib.request import urlopen
from selenium import webdriver
import time
import numpy as np
import random
import os

RAW_PATH="../data/raw/"
INTERIM_PATH="../data/interim/"
PROCESSED_PATH="../data/processed/"
MODEL_PATH="../models/"
CRM_PATH='/Users/alamhanz/Documents/My_files/personal project/education-space/src/chromedriver'
MAIN_URL="http://dapo.dikdasmen.kemdikbud.go.id/sp"

def get_url_area(URL):
    xr1=random.randint(5,10)
    xr2=random.randint(3,xr1)
    browser = webdriver.Chrome(CRM_PATH)
    
    time.sleep(xr2)
    browser.get(URL)
    xr1=random.randint(7,(xr1+xr2))
    xr2=random.randint(4,xr1)
    time.sleep(xr1+xr2)
    html_source = browser.page_source
    browser.close()

    #Store the contents of the website under doc
    doc = lh.fromstring(html_source)
    #Parse data that are stored between <tr>..</tr> of HTML
    area = [s.text_content() for s in doc.xpath("//tr//a")]
    url_area = [(MAIN_URL[:-3]+s).strip() for s in doc.xpath("//tr//a/@href")]

    data=pd.DataFrame({'areas':area,'url_areas':url_area})
    return data

# os.environ["webdriver.chrome.driver"] = 
file_name='url_dikdas_kabkot1.csv'
file_name_output='url_dikdas_kec4.csv'
# "url_dikdas_kec.csv"

dd_kab_kot2=pd.read_csv(RAW_PATH+file_name)
d1=dd_kab_kot2[dd_kab_kot2.kab_kota=='Kab. Garut']
list_dd=[]

# d1=dd_kab_kot2.iloc[[ii]]
d1['key']=1
d1.columns=['provinsi','kab_kota','url','key']
url1=d1['url'].tolist()[0]
d1=d1[['provinsi','kab_kota','key']]
print(url1)

d2=get_url_area(url1)
d2['key']=1
dmerg=pd.merge(d1, d2,on='key')
dmerg=dmerg[['provinsi','kab_kota','areas','url_areas']]
dmerg.columns=['provinsi','kab_kota','kecamatan','url']
list_dd.append(dmerg)
    
print('saving ...')

dd_kec=pd.concat(list_dd)
dd_kec.to_csv(RAW_PATH+file_name_output,index=False)

print('done')