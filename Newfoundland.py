import requests
import json
import pandas as pd
import time
from datetime import date

####API Pull####
requestNL = requests.get("https://services8.arcgis.com/aCyQID5qQcyrJMm2/arcgis/rest/services/Prov_Covid_Daily_Stats_Public/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json").json()
contentNL = json.dumps(requestNL, indent = 4, sort_keys=True)

####Building the dataframe####
dataNL = requestNL['features']
dfNL = pd.concat([pd.DataFrame(l) for l in dataNL], axis=1, sort=True).T

i = 0
dfGeometry = pd.DataFrame()
dfAttributes = pd.DataFrame()
while i < len(dataNL):
    nesteddict = dataNL[i]
    dfAttributes = pd.concat([dfAttributes, pd.DataFrame(nesteddict['attributes'], index=[i])])
    if 'geometry' in nesteddict:
        dfGeometry = pd.concat([dfGeometry, pd.DataFrame(nesteddict['geometry'], index=[i])])
    else:
        dfGeometry = pd.concat([dfGeometry, pd.DataFrame()])
    i += 1
            
dfNewfoundland = pd.concat([dfAttributes, dfGeometry], axis=1)

####Cleaning####
dfNewfoundland['date_of_update']=dfNewfoundland['date_of_update'].apply(lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(x/1000.0)))
dfNewfoundland = dfNewfoundland.sort_values(by=['date_of_update'])
dfNewfoundland = dfNewfoundland.reset_index(drop=True)

####print to csv####
timestamp = date.today()
dfNewfoundland.to_csv('C:/..._{}.csv'.format(timestamp))




