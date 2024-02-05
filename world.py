import requests
from bs4 import BeautifulSoup

import pandas as pd

url = 'https://www.worldometers.info/world-population/population-by-country/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.find('table', {'id':'example2'}).find('tbody').find_all('tr')

countries_list = []

for row in rows:
    dic = {}

    dic['Country'] = row.find_all('td')[1].text
    dic['Population (2023)'] = row.find_all('td')[2].text
    dic['Yearly Change'] = row.find_all('td')[3].text
    dic['Net Change'] = row.find_all('td')[4].text
    dic['Density (P/km²)'] = row.find_all('td')[5].text
    dic['Land Area (km²)'] = row.find_all('td')[6].text
    dic['Migrants'] = row.find_all('td')[7].text
    dic['Fert. Rate'] = row.find_all('td')[8].text
    dic['Med. Age'] = row.find_all('td')[9].text
    dic['Urban Pop %'] = row.find_all('td')[10].text
    dic['World Share'] = row.find_all('td')[11].text

    countries_list.append(dic)

print(countries_list[0])

df = pd.DataFrame(countries_list)
df.to_csv('world_data.csv', index=False)