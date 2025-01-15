#Downloaded Colab Notebook

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://asn.flightsafety.org/asndb/cat/WXT/3"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
}

dates = []
times = []
locations = []

for page in range(5, 6):
  response = requests.get(f"https://asn.flightsafety.org/asndb/cat/WXT/{page}", headers=headers).content
  soup = BeautifulSoup(response, "html.parser")
  for link in soup.find_all("a"):
    link = link.get('href')
    if "/wikibase/" in link and 'web_db' not in link:
      get_loc = requests.get(f"https://asn.flightsafety.org/{link}", headers=headers).content
      loc_soup = BeautifulSoup(get_loc, 'html.parser')
      items = loc_soup.find_all('td', class_='caption')
      dates.append(items[1].get_text())
      items = []
      for item in loc_soup.find_all('td'):
        items.append(item.get_text())
      for x in range(len(items)):
        if (items[x] == "Time:"):
          times.append(items[x+1])
      items = []
      for item in loc_soup.find_all('td'):
        items.append(item.get_text())
      for x in range(len(items)):
        if (items[x] == "Location:"):
          locations.append(items[x+1])

locations = [loc.replace('\n', '').replace('\t', '').replace('\xa0', '').strip() for loc in locations]
len(dates), len(times), len(locations)
df = pd.DataFrame(data=(dates, times, locations)).T
df.columns = ["Date", "Time", "Location"]
df

df.loc[72]