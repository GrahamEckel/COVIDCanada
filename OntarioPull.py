import requests
import json
import pandas as pd
from datetime import date

####API Pull####
requestStatus = requests.get("https://data.ontario.ca/api/3/action/datastore_search?resource_id=ed270bb8-340b-41f9-a7c6-e8ef587e6d11&limit=999999").json()
contentStatus = json.dumps(requestStatus, indent = 4, sort_keys=True)

requestConfirmed = requests.get("https://data.ontario.ca/api/3/action/datastore_search?resource_id=455fd63b-603d-4608-8216-7d8647f43350&limit=999999").json()
contentConfirmed = json.dumps(requestConfirmed, indent = 4, sort_keys=True)

####data####
dataStatus = requestStatus['result']['records']
dfStatus = pd.DataFrame(dataStatus)

dataConfirmed = requestConfirmed['result']['records']
dfConfirmed = pd.DataFrame(dataConfirmed)

####print to csv####
timestamp = date.today()
dfStatus.to_csv('C:/Users/graha/Google Drive/1. Math MSc/Covid Analysis/Provincial Data/OntarioStatus_{}.csv'.format(timestamp))
dfConfirmed.to_csv('C:/Users/graha/Google Drive/1. Math MSc/Covid Analysis/Provincial Data/OntarioConfirmed_{}.csv'.format(timestamp))


