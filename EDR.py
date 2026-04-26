import os
import xarray as xr
import pandas as pd
from sklearn.metrics.pairwise import haversine_distances
from math import radians

plymouth_data = pd.read_excel(r"C:\Users\harsh\Downloads\Copy of Plymouth US Available Data.xlsx")
plymouth_regions = plymouth_data['Map Region'].unique()
plymouth_dict = {
    region: {
      row['Municipality']: {
          'Latitude': row['Latitude'],
          'Longitude': row['Longitude'],
          'Pixel X': row['Pixel X'],
          'Pixel Y': row['Pixel Y']
      } for _, row in plymouth_data[plymouth_data['Map Region'] == region].iterrows()
    }
    for region in plymouth_regions
}

def remove_duplicates(dataset):
  x = 0
  while x < len(dataset):
    datetime_x = str(dataset['Year'][x]) + str(dataset['Month'][x]) + str(dataset['Day'][x]) + str(dataset['Time'][x])
    y = 0
    while y < len(dataset):
      datetime_y = str(dataset['Year'][y]) + str(dataset['Month'][y]) + str(dataset['Day'][y]) + str(dataset['Time'][y])
      delta_lat = abs(dataset['Latitude'][y] - dataset['Latitude'][x])
      delta_lon = abs(dataset['Longitude'][y] - dataset['Longitude'][x])
      if (x != y and datetime_x == datetime_y and delta_lat < 3 and delta_lon < 3):
        dataset = dataset.drop(y).reset_index(drop=True)
      else:
        y+=1
    x+=1

  return dataset

def haversine_distance(lat1, lon1, lat2, lon2):
  X, Y = [lat1, lon1], [lat2, lon2]
  dist = haversine_distances([[radians(x) for x in X], [radians(y) for y in Y]])
  dist = dist[0][1] * 6371 * (5/8)
  return dist

def find_nearest(data, classname):
  min_distances, data_locations  = [], []

  for x in range(len(data)):
    min_dist = 13000
    data_loc = ""
    lat, lon = data['Latitude'][x], data['Longitude'][x]
    for region in [item for item in plymouth_dict.keys()]:
      locations = [item for item in plymouth_dict[region].keys()]
      for location in locations:
        lat2, lon2 = plymouth_dict[region][location]['Latitude'], plymouth_dict[region][location]['Longitude']
        dist = haversine_distance(lat, lon, lat2, lon2)
        if dist < min_dist:
          min_dist = dist
          data_loc = location
    min_distances.append(min_dist)
    data_locations.append(data_loc)

  data['Distance to Data'] = min_distances
  data['Data Location'] = data_locations
  data = data[data['Distance to Data'] < 50].reset_index(drop=True)
  data['Class'] = classname
  return data

file_paths = os.listdir(r'C:/Users/harsh/MADIS_DATA/point/acars/netcdf/')

data = pd.DataFrame(columns=['Year', 'Month', 'Day', 'Time', 'Latitude', 'Longitude', 'Altitude', 'EDR * 100'])
start, end, classname = 22, 100, 'Medium Turbulence'

for x in range(9401, 13000):
    print(x)
    year, month, day, hour = file_paths[x][:4], file_paths[x][4:6], file_paths[x][6:8], file_paths[x][9:11]
    curr_path = f'C:/Users/harsh/MADIS_DATA/point/acars/netcdf/{file_paths[x]}'
    ds = xr.open_dataset(curr_path, engine="scipy", decode_times=False)
    latitudes = [round(item.item(), 2) for item in ds['latitude']]
    longitudes = [round(item.item(), 2) for item in ds['longitude']]
    altitudes = [round(item.item() * 3.28084, 2) for item in ds['altitude']]
    EDR = [round(item.item(), 2) * 100 for item in ds['medEDR']]
    years = [year] * len(EDR)
    months = [month] * len(EDR)
    days = [day] * len(EDR)
    times = [hour] * len(EDR)

    curr_data = pd.DataFrame({'Year': years, 'Month': months, 'Day': days, 'Time': times,
    'Latitude': latitudes, 'Longitude': longitudes,'Altitude': altitudes, 'EDR * 100': EDR})
    curr_data = curr_data[(curr_data['EDR * 100'] >= start) & (curr_data['EDR * 100'] < end) & (curr_data['Altitude'] > 20000)]
    data = pd.concat([data, curr_data], ignore_index=True)

    if (x > 0 and x % 100 == 0):
      print(data)
      data = remove_duplicates(data)
      data = data.dropna().reset_index(drop=True)
      data = find_nearest(data, classname)
      print(data)
      data.to_excel(f"C:/Users/harsh/{classname}{x/100}.xlsx")
      data = pd.DataFrame(columns=['Year', 'Month', 'Day', 'Time', 'Latitude', 'Longitude', 'Altitude', 'EDR * 100'])



    