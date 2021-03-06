## Get All Urls
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
from selenium.webdriver.support.select import Select

RAW_PATH="../data/raw/"
RAW_KEC_PATH=RAW_PATH+"kecamatan_partition_to_get_URL_school/"

INTERIM_PATH="../data/interim/"
INTERIM_PATH2="../data/interim/school_url_All/"
PROCESSED_PATH="../data/processed/"
MODEL_PATH="../models/"
CURR_PATH=os.getcwd()
# CRM_PATH=CURR_PATH+'/chromedriver'
CRM_PATH=CURR_PATH+'/chromedriver.exe'
MAIN_URL="http://dapo.dikdasmen.kemdikbud.go.id/sp"

def get_url_area(URL):
	xr1=random.randint(1,4)
	xr2=random.randint(1,xr1)
	browser = webdriver.Chrome(CRM_PATH)
	
	time.sleep(xr2)
	k=0
	tr=1
	good=0
	while k==0 and tr<=8:
		k=1
		try:
			browser.get(URL)
			good=1
		except:
			browser.close()
			browser = webdriver.Chrome(CRM_PATH)
			time.sleep(5)
			print('trial ',tr, 'fail')
			k=0
			tr+=1
	xr1=random.randint(4,8)
	xr2=random.randint(2,xr1)
	time.sleep(xr1+xr2)

	browse=True
	try:
		test_select=Select(browser.find_element_by_id("selectJenjang"))
		test_select.select_by_visible_text('SMA')
		xr2=random.randint(2,xr1)
		time.sleep(xr1+xr2)
		test_select.select_by_visible_text('Semua Jenjang')
		xr1=random.randint(1,xr2)
		test_select.select_by_visible_text('SD')
		xr1=random.randint(1,xr2+xr1)
		test_select.select_by_visible_text('Semua Jenjang')
		xr1=random.randint(1,6)
		xr2=random.randint(3,9)
		time.sleep(xr1+xr2)
	except:
		browse=False

	if browse:
		html_source = browser.page_source
		browser.close()

		#Store the contents of the website under doc
		doc = lh.fromstring(html_source)
		#Parse data that are stored between <tr>..</tr> of HTML
		area = [s.text_content() for s in doc.xpath("//tr//a")]
		url_area = [(MAIN_URL[:-3]+s).strip() for s in doc.xpath("//tr//a/@href")]
		other_info = [s.text_content() for s in doc.xpath("//tr//td")]

		if good==1:
			data_selected=pd.DataFrame({'nama_sekolah':area,'url_sekolah':url_area})
			## "-9" because the last rows is "Total Rows"
			df_other_info=pd.DataFrame([other_info[:-9][i:i + 14] for i in range(0, len(other_info[:-9]), 14)],
						columns=['no','nama_sekolah','npsn','bp','status',
								 'last_sync','jml_sync','pd','rombel','guru',
								 'pegawai','ruang_kelas','ruang_lab','ruang_perpus'])
			all_info_sekolah=pd.merge(df_other_info,data_selected,on='nama_sekolah',how='left')
		else:
			all_info_sekolah=[]
	else:
		all_info_sekolah=[]
	return all_info_sekolah,browse



file_name=input('get data :')
dd_kab_kot2=pd.read_csv(RAW_KEC_PATH+file_name)

## kab kot to Kecamatan
# list_dd=[]
for ii in dd_kab_kot2.index.tolist():
	d1=dd_kab_kot2.iloc[[ii]]
	d1['key']=1
	d1.columns=['provinsi','kab_kota','kecamatan','url','key']
	url1=d1['url'].tolist()[0]
	kab1=d1['kab_kota'].tolist()[0]
	kab1=kab1.replace('. ','_')
	if kab1 not in os.listdir(INTERIM_PATH2):
		os.mkdir(INTERIM_PATH2+kab1)
	fkec1=d1['kecamatan'].tolist()[0]+'.csv'
	fkec1=fkec1.replace('. ','_')
	fkec1=fkec1.replace('/','_atau_')
	if fkec1 in os.listdir(INTERIM_PATH2+kab1):
		print('has done')
	else:
		d1=d1[['provinsi','kab_kota','kecamatan','key']]
		print(url1)

		browse_result=get_url_area(url1)
		d2=browse_result[0]

		if browse_result[1]:
			d2['key']=1
			dmerg=pd.merge(d1, d2,on='key')
			dmerg=dmerg[['provinsi','kab_kota','kecamatan','nama_sekolah','npsn','bp','status',
								 'last_sync','jml_sync','pd','rombel','guru',
								 'pegawai','ruang_kelas','ruang_lab','ruang_perpus','url_sekolah']]
		#     list_dd.append(dmerg)
			dmerg.to_csv(INTERIM_PATH2+kab1+'/'+fkec1,index=False)
		else:
			print(ii," NOT SUCCESS")

print('done')