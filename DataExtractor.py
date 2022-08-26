
from pandas import json_normalize

import requests

url = "https://stagingapp.techdestination.com/export_all_companies"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload,verify = False)

companies_json=response.json()

df = json_normalize(companies_json['data']['companies'])

# df = pd.DataFrame({'col1': col1, 'col2': col2})

fname = 'Companies_data.csv'

df.to_csv(fname, index=False)


url = "https://stagingtechleads.techdestination.com/export_all_techleads"

headers = { }

response = requests.request("GET", url, headers=headers, data=payload,verify = False)
techleads_json=response.json()
df = json_normalize(techleads_json['data']['techleads'])

fname = 'TechLeads_data.csv'

df.to_csv(fname, index=False)
