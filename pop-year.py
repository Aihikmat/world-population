import requests
from bs4 import BeautifulSoup

import pandas as pd

url = 'https://www.worldometers.info/world-population/world-population-by-year/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.find('table').find('tbody').find_all('tr')

countries_list = []

for row in rows:
    dic = {}

    dic['Year'] = row.find_all('td')[0].text
    dic['World Population'] = row.find_all('td')[1].text
    dic['Yearly Change %'] = row.find_all('td')[2].text
    dic['Net Change'] = row.find_all('td')[3].text
    dic['Density (P/km²)'] = row.find_all('td')[4].text

    countries_list.append(dic)

print(countries_list[0])

df = pd.DataFrame(countries_list)
df.to_csv('pop_year.csv', index=False)