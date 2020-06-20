import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import date 

####Grabbing the html####
URL = 'https://www.alberta.ca/stats/covid-19-alberta-statistics.htm'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='data-export')

####Parsing####
txt = str(results)
subtxt1 = "[["
subtxt2 = "]]"
data = txt[txt.find(subtxt1)+1 : txt.find(subtxt2)-1].replace('"', '')
df = pd.DataFrame([x.split('[') for x in data.split('\n')])
df = df.drop(df.columns[[0]], axis=1)

####Building the dataframe####
dfAlberta = pd.DataFrame()
i = 1
while i < len(df.columns):
    dfi = df.filter(df.columns[[i]], axis=1)
    explode = dfi[dfi.columns[0]].str.split(',').apply(pd.Series, 1).stack()
    explode.reset_index(drop=True, inplace=True)
    dfAlberta = pd.concat([dfAlberta, explode], ignore_index=True, axis=1)
    i += 1

####Cleaning####
dfAlberta = dfAlberta[:-1]
dfAlberta = dfAlberta.replace({']':''}, regex=True)    
dfAlberta = dfAlberta.rename(columns={0: "Date Reported", \
                                      1: "Alberta Health Services Zone", \
                                      2: "Gender", \
                                      3: "Age group", \
                                      4: "Case status", \
                                      5: "Case type"})

####Print to csv####
timestamp = date.today()
dfAlberta.to_csv('C:/Users/..._{}.csv'.format(timestamp))
    

