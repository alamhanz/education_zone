import pandas as pd
import matplotlib.pyplot as plt
import requests
import lxml.html as lh
import pandas as pd
from urllib.request import urlopen
# from selenium import webdriver
import time
import numpy as np
import random
import os
# from bs4 import BeautifulSoup
from lxml.etree import tostring

RAW_PATH="../data/raw/"
RAW_KEC_PATH=RAW_PATH+"kecamatan_partition_to_get_URL_school/"
INTERIM_PATH="../data/interim/"
INTERIM_PATH2="../data/interim/school_url_All/"
INTERIM_PATH_TMP="../data/interim/tmp/"

PROCESSED_PATH="../data/processed/"
MODEL_PATH="../models/"
CRM_PATH='../src/chromedriver'

# https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
def get_long_lat(main_school_url):
    try :
        req = requests.get(main_school_url)
        html_source=req.text
        doc = lh.fromstring(html_source)
        ss=doc.xpath("//div[@class='tab-content']")
        ss0=ss[0]
        ss0_content=ss0.text_content()
        res=','.join([k.strip() for k in ss0_content.split('\n') 
                      if ('lintang' in k.lower())|('bujur' in k.lower())])
    except:
        print('miss : '+ main_school_url)
        res=np.nan
    return res

part=input('get part : ')

fn=INTERIM_PATH_TMP+'20190901_sekolah_genap2019_data_latlong_all_notyet_'+str(part)+'.csv'

df0=pd.read_csv(fn)
df0=df0.reset_index()


## Run some of it
for i in range(200):
    L0=time.time()    
    df=df0[0+(i*300):300+(i*300)]
    if len(df)==0:
        print('STOP')
        break
    
    df['coordinate']=df.url_sekolah.apply(lambda x : get_long_lat(x))
    df.to_csv(INTERIM_PATH_TMP+'data_all_school_coord'
              +str(part)+'_'+str(i)+'.csv',index=False)
    print(str(i)+" is done in "+str(time.time()-L0))