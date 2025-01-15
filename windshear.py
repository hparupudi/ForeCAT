#Downloaded Colab Notebook

import pandas as pd
import numpy as np
#Storing location data in three arrays
data = pd.read_excel("/content/location_data1.xlsx", index_col=0)
dates = data["Date"].to_numpy()
locations = data["Location"].to_numpy()
regions = data["Region"].to_numpy()
elevations = data["Elevation"].to_numpy()
pixels_X = data["PixelX"].to_numpy()
pixels_Y = data["PixelY"].to_numpy()
times = data["Time"].to_numpy()

#Store incidents by region and year in 2D numpy array
new_regions, temp_years = [], []
#Creates dictionary that maps each specific Plymouth region to a general region eg. US -> North America
region_name_dict = {"Contiguous US": "North America", "Northeast": "North America", "Mid-Atlantic": "North America", "Southeast": "North America", "Midwest": "North America","Southern Plains": "North America",
"Northwest": "North America", "Southwest": "North America", "Alaska": "North America", "Hawaii": "North America","Eastern Canada": "North America","Western Canada": "North America", "Northern Canada": "North America", "Canada": "North America",
"North America": "North America", "Central America": "South America", "South America": "South America", "Europe": "Europe", "Asia": "Asia","East Asia": "Asia", "West Asia": "Asia", "North Asia": "Asia",
"Southeast Asia": "Asia", "Africa": "Africa","North Africa": "Africa","South Africa": "Africa","Middle East": "Asia","Australia": "Oceania","West Pacific": "Oceania"}
region_names = ["North America", "South America", "Europe", "Asia", "Africa", "Oceania"]
data_arr = np.zeros([23, 6])
counter = 0
for x in range(len(regions)):
  if regions[x] in region_name_dict:
    new_regions.append(region_name_dict[regions[x]])
  else:
    counter+=1
  temp_years.append(int(dates[x][len(dates[x]) - 4:]))
  data_arr[temp_years[x-counter] - 2002][region_names.index(new_regions[x-counter])]+=1

df = pd.DataFrame({"Region": region_names})
for x in range(0, 23):
  df[2002 + x] = data_arr[x]

#Visualize incidents over time
import seaborn as sns
import matplotlib.pyplot as plt
region_names = ["North America", "South America", "Europe", "Asia", "Africa", "Oceania"]
plt.figure(figsize=(10, 7))
sns.set_theme(style='darkgrid')
colors = ['#4B88A2', '#6FB98F', '#FFD166', '#EF476F', '#8338EC', '#3A86FF']
x_data = [int(x) for x in range(2002, 2025)]
y_data = [int(x) for x in range(0, 55, 5)]
bottom = 0
turbulence_label = [int(x) for x in range(0, 23)]
for x in range(0, 6):
  data = df.iloc[x].iloc[1:]
  bar = sns.barplot(data=data, color=colors[x], bottom=bottom, label=region_names[x])
  bottom+=data.values
bar.set_title("Turbulence Incidents 2002-2024", fontsize=16, pad=20)
bar.set(xlabel="Year", ylabel="Reported Turbulence Incidents")
plt.xticks(turbulence_label, x_data, rotation=90)
plt.yticks(y_data)
plt.legend(title="Region", loc="upper left")

#Splitting Date into Day, Month, Year for CAT Dataset
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
days = []
mons = []
years = []
for date in dates:
  year = date[:4]
  month = months[int(date[5:7]) - 1]
  day = date[8:10]
  years.append(year)
  mons.append(month)
  days.append(day)

#Generating random date for Non-CAT Dataset
import random

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
random_year = random.randint(2002, 2024)
mth_idx = random.randint(0, 11)
random_month = months[mth_idx]
random_day = random.randint(1, 28)

print(f"Random Date: {random_year} {random_month} {random_day}")

#Remove impossible dates
for x in range(len(years)):
  if mons[x] == "Feb" and (days[x] == 30 or days[x] == 29):
    days[x] = random.randint(1, 28)
    print(days[x])

#Removes locations with no data
new_regions, new_pixelsX, new_pixelsY, new_years, new_mons, new_days = np.array([[], [], [], [], [], []])

for x in range(len(regions)):
  if (years[x] != 2023 or (years[x] == 2023 and mons[x] != 'Apr' and mons[x] != 'May' and mons[x] != 'Jun' and mons[x] != 'Jul')):
    new_regions = np.append(new_regions, regions[x])
    new_pixelsX = np.append(new_pixelsX, pixels_X[x])
    new_pixelsY = np.append(new_pixelsY, pixels_Y[x])
    new_years = np.append(new_years, years[x])
    new_mons = np.append(new_mons, mons[x])
    new_days = np.append(new_days, days[x])

regions = new_regions
pixels_X = new_pixelsX
pixels_Y = new_pixelsY
years = new_years.astype(int)
mons = new_mons
days = new_days.astype(int)

#Sets up arrays to store data
lowerS_arr = []
lowerD_arr = []
upperD_arr = []
upperS_arr = []

#Stores locations w/ no data to be removed from other time
#no_data = []

#Creates dictionary for crop radius for each location
region_dict = {
      "Contiguous US": 75,
      "Northeast": 100,
      "Mid-Atlantic": 100,
      "Southeast": 150,
      "Midwest": 150,
      "Southern Plains": 100,
      "Northwest": 100,
      "Southwest": 150,
      "Alaska": 200,
      "Hawaii": 200,
      "Eastern Canada": 100,
      "Western Canada": 100,
      "Northern Canada": 100,
      "Canada": 75,
      "North America": 75,
      "Central America": 150,
      "South America": 120,
      "Europe": 50,
      "Asia": 50,
      "East Asia": 100,
      "West Asia": 100,
      "North Asia": 100,
      "Southeast Asia": 200,
      "Africa": 300,
      "North Africa": 300,
      "South Africa": 300,
      "Middle East": 100,
      "Australia": 100,
      "West Pacific": 200,
      "Antarctica": 200,
      "Arctic": 200
  }

dpi = 141

#Function to save Plymouth Map to Google Drive
def save_img(img, img_num):
  width, height = 1185, 874
  plt.figure(figsize=(width / dpi, height / dpi))
  plt.imshow(img)
  plt.axis('off')
  img = plt.savefig(fname=f'/content/drive/MyDrive/CAT Dataset/{img_num}.png', dpi=dpi, bbox_inches='tight', pad_inches=0)
  return img

import pytesseract
import cv2
from PIL import Image
from pytesseract import Output
import math

counter = []

def format_img(img, img_num):
    data_pixels = []
    left_x, right_x = 10, 900
    top_y, bottom_y = 50, 640

    width, height = img.size
    pixel_X = pixels_X[img_num]
    pixel_Y = pixels_Y[img_num]
    constant = region_dict[regions[img_num]]
    directions = [pixel_X - constant, pixel_Y - constant, pixel_X + constant, pixel_Y + constant]

    for x in range(len(directions)):
      if x % 2 == 0:
        directions[x] = max(directions[x], left_x)
        directions[x] = min(directions[x], right_x)
      else:
        directions[x] = max(directions[x], top_y)
        directions[x] = min(directions[x], bottom_y)

    rgb_img = img.convert('RGB')

    for x in range(width):
      for y in range(height):
        r, g, b = rgb_img.getpixel((x, y))
        if r > 150 and g < 10 and b < 10:
          rgb_img.putpixel((x, y), (255, 255, 255))
        if r < 255 or g < 255 or b < 255:
          rgb_img.putpixel((x, y), (0, 0, 0))

    cropped_img = rgb_img.crop((directions[0], directions[1], directions[2], directions[3]))
    return cropped_img

def get_data(img, img_num, data_type):
  curr_coords = []
  newStr = []
  options = "--psm 11"

  cropped_img = format_img(img, img_num)
  width, height = cropped_img.size
  new_width, new_height = width * 3, height * 3
  center = [new_width / 2, new_height / 2]
  cropped_img = cropped_img.resize((new_width, new_height), Image.BICUBIC)
  plt.imshow(cropped_img)
  plt.axis('off')

  curr_vals = pytesseract.image_to_string(cropped_img, config=options)
  curr_vals = curr_vals.split()
  curr_data = pytesseract.image_to_boxes(cropped_img, config=options, output_type=Output.DICT)

  new_vals = []

  for val in curr_vals:
    if val.isdigit():
      new_vals.append(int(val))

  curr_vals = new_vals
  left = 0
  top = 0

  if 'left' in curr_data.keys():
    for x in range(len(curr_data['left'])):
      if ((abs(curr_data['left'][x] - left) > 30) or (abs(curr_data['top'][x] - top) > 30)):
        curr_loc = [curr_data['left'][x], new_height - curr_data['top'][x]]
        curr_coords.append([curr_loc[0], curr_loc[1]])
        left = curr_data['left'][x]
        top = curr_data['top'][x]

  new_curr_vals = []
  new_curr_coords = []

  for x in range(len(curr_vals)):
    if (data_type == "lowerS" or data_type =="upperS"):
      if (curr_vals[x] <= 130):
        if x < len(curr_coords):
          new_curr_vals.append(curr_vals[x])
          new_curr_coords.append(curr_coords[x])
    else:
      if (curr_vals[x] <= 360):
        if x < len(curr_coords):
          new_curr_vals.append(curr_vals[x])
          new_curr_coords.append(curr_coords[x])

  curr_vals = new_curr_vals
  curr_coords = new_curr_coords

  min_dist = 1000
  min_coords = [0, 0]
  val = 0
  if len(curr_coords) >= 1:
    for x in range(len(curr_coords)):
      dist = math.sqrt(pow(abs(curr_coords[x][0] - center[0]), 2) + pow(abs(curr_coords[x][1] - center[1]), 2))
      if dist < min_dist:
        min_dist = dist
        min_coords = curr_coords[x]
    val = curr_vals[curr_coords.index(min_coords)]

  if data_type == "lowerS":
    lowerS_arr.append(val)

  elif data_type == "upperS":
    upperS_arr.append(val)

  elif data_type == "lowerD":
    lowerD_arr.append(val)

  else:
    upperD_arr.append(val)

def remove_empty():
  global regions, elevations
  no_data = []
  for x in range(len(lowerS_arr)):
    if len(lowerS_arr[x]) == 0 or len(lowerD_arr[x]) == 0 or len(upperS_arr[x]) == 0 or len(upperD_arr[x]) == 0:
      no_data.append(x)

  new_regions = []
  new_elevations = []

  for x in range(len(lowerS_arr)):
    if x not in no_data:
      new_regions.append(regions[x])
      new_elevations.append(elevations[x])

  regions = new_regions
  elevations = new_elevations

  for x in range(len(no_data)):
    no_data[x]-=x
    lowerS_arr.remove(lowerS_arr[no_data[x]])
    lowerD_arr.remove(lowerD_arr[no_data[x]])
    upperS_arr.remove(upperS_arr[no_data[x]])
    upperD_arr.remove(upperD_arr[no_data[x]])

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import urllib.request
import io
import matplotlib.pyplot as plt
from datetime import datetime

#Configuring selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--diable-dve-shm-uage')

#Function to find image data
def find_image(region, pressure, attr, year, month, day, time):
  driver = webdriver.Chrome(options=options)
  url="https://vortex.plymouth.edu/myowxp/upa/pltmap-a.html"
  driver.get(url)

  Select(driver.find_element("name", "re")).select_by_visible_text(f"{region}")
  Select(driver.find_element("name", "le")).select_by_visible_text(f"{pressure}")
  Select(driver.find_element("name", "va")).select_by_visible_text(f"{attr}")
  Select(driver.find_element("name", "yy")).select_by_visible_text(f"{year}")
  Select(driver.find_element("name", "mm")).select_by_visible_text(f"{month}")
  Select(driver.find_element("name", "dd")).select_by_visible_text(f"{day}")
  Select(driver.find_element("name", "hh")).select_by_visible_text(f"{time}")
  Select(driver.find_element("name", "sc")).select_by_visible_text(".7")

  driver.find_element(by=By.TAG_NAME, value='input').click()
  map_img = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//img[@alt='[GIF]']"))
  )

  map_img = map_img.get_attribute("src")
  driver.quit()
  img = urllib.request.urlopen(map_img).read()
  img = Image.open(io.BytesIO(img))
  return img

#Find closest time (0Z, 12Z, or next day 0Z) for collecting data
def find_time(years, months, days, times, x):
  year = years[x]
  month = mons[x]
  day = int(days[x])
  mth_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  time_0Z = datetime(year=1900, month=1, day=1, hour=0, minute=0)
  time_12Z = datetime(year=1900, month=1, day=1, hour=12, minute=0)
  time_0Z_2 = datetime(year=1900, month=1, day=2, hour=0, minute=0)
  time = datetime.strptime(times[x], "%H:%M")
  delta_0Z = abs(time - time_0Z).total_seconds()
  delta_12Z = abs(time - time_12Z).total_seconds()
  delta_0Z_2 = abs(time - time_0Z_2).total_seconds()
  min_delta = min(delta_0Z, delta_12Z, delta_0Z_2)
  if delta_0Z == min_delta:
    data_time = "0 Z"
  elif delta_12Z == min_delta:
    data_time = "12 Z"
  else:
    data_time = "0 Z"
    if (int(day) < mth_days[months.index(month)]):
      day+=1
    else:
      if month != 12:
        day=1
        month+=1
      else:
        day=1
        month=1
        year+=1
  return year, month, day, data_time

#Loop to find image data for every location in dataset
for x in range(0, 200):
  #year, month, day, data_time = find_time(years, months, days, times, x)
  year, month, day, data_time = random_year, random_month, random_day, "0 Z"
  img = find_image(regions[x], "700 mb", "Wind Speed", year, month, day, data_time)
  get_data(img, x, 'lowerS')
  img2 = find_image(regions[x], "700 mb", "Wind Direction", year, month, day, data_time)
  get_data(img2, x, 'lowerD')
  img3 = find_image(regions[x], "200 mb", "Wind Speed", year, month, day, data_time)
  get_data(img3, x, 'upperS')
  img4 = find_image(regions[x], "200 mb", "Wind Direction", year, month, day, data_time)
  get_data(img4, x, 'upperD')
  #clean_arr(x)
#width, height = img.size
#print(width, height)

#Remove unrealistic values + locations w/ no data
x = 0
while x < len(lowerS_arr):
  if lowerS_arr[x]== 0 or lowerD_arr[x] == 0 or upperS_arr[x] == 0 or upperD_arr[x] == 0:
    lowerS_arr.remove(lowerS_arr[x])
    lowerD_arr.remove(lowerD_arr[x])
    upperS_arr.remove(upperS_arr[x])
    upperD_arr.remove(upperD_arr[x])
  elif (lowerS_arr[x] < 10 or upperS_arr[x] < 10 or lowerS_arr[x] > 100 or upperS_arr[x] > 100) and abs(lowerS_arr[x] - upperS_arr[x]) > 20:
    lowerS_arr.remove(lowerS_arr[x])
    lowerD_arr.remove(lowerD_arr[x])
    upperS_arr.remove(upperS_arr[x])
    upperD_arr.remove(upperD_arr[x])
  elif (lowerD_arr[x] < 50 or upperD_arr[x] < 50) and abs(lowerD_arr[x] - upperD_arr[x]) > 100:
    lowerS_arr.remove(lowerS_arr[x])
    lowerD_arr.remove(lowerD_arr[x])
    upperS_arr.remove(upperS_arr[x])
    upperD_arr.remove(upperD_arr[x])
  else:
    x+=1
print(len(lowerS_arr))

num = 10
print(f"Lower S: {lowerS_arr[num]}")
print(f"Lower D: {lowerD_arr[num]}")
print(f"Upper S: {upperS_arr[num]}")
print(f"Upper D: {upperD_arr[num]}")

import numpy as np
import matplotlib.pyplot as plt
import math

#Initialize vector map & windshear dataframe
vectorMap = []
windshear = []

def degtoBearing (angle): #Turns degrees into bearing angles
    #Want to : [0, 45, 90, 135, 180, 225, 270, 315, 0] - > [90, 45, 0, 315, 270, 225, 180, 135, 90]
    angle = angle % 360 #Corresponding angle from 0-359
    bearingAngle = 360 - angle #[0, 45, 90, 135, 180, 225, 270, 315, 0] -> [360, 315, 270, 225, 180, 135, 90, 45, 360]
    bearingAngle = bearingAngle - 270 #[360, 315, 270, 225, 180, 135, 90, 45, 360] -> [90, 45, 0, -45, -90, -135, -180, -225, 90]

    if bearingAngle < 0: #If negative
      bearingAngle = bearingAngle + 360 #[90, 45, 0, -45, -90, -135, -180, -225, 90] -> [90, 45, 0, 315, 270, 225, 180, 135, 90]

    return bearingAngle

def bearingtoDeg (bearingAngle): #Turns bearing angles into degrees
    #Want to : [90, 45, 0, 315, 270, 225, 180, 135, 90] - > [0, 45, 90, 135, 180, 225, 270, 315, 0]
    bearingAngle = bearingAngle % 360 #Corresponding angle from 0-359
    angle = 360 - bearingAngle #[90, 45, 0, 315, 270, 225, 180, 135, 90] -> [270, 335, 360, 45, 90, 135, 180, 225, 270]
    angle = angle - 270 #[270, 335, 360, 45, 90, 135, 180, 225, 270] -> [0, 45, 90, -225, -180, -135, -90, -45, 0]

    if angle < 0: #If negative
      angle = angle + 360 #[0, 45, 90, -225, -180, -135, -90, -45, 0] -> [0, 45, 90, 135, 180, 225, 270, 315, 0]

    return angle


def windShear (lowerS, lowerD, upperS, upperD): #Calculate wind shear
    lowerD = np.deg2rad(bearingtoDeg(lowerD)) #Turns bearing to rad
    lowerD = np.array([np.cos(lowerD), np.sin(lowerD)]) #Turns into unit vector
    upperD = np.deg2rad(bearingtoDeg(upperD)) #Turns bearing to rad
    upperD = np.array([np.cos(upperD), np.sin(upperD)]) #Turns into unit vector

    lowerV = lowerD * lowerS #Lower wind vector
    upperV = upperD * upperS #Upper wind vector

    windShear = upperV - lowerV #Wind shear: Difference in wind vectors
    for i in range(len(windShear)):
      windShear[i] = round(windShear[i], 2)

    return windShear

def dataArray (lowerS, lowerD, upperS, upperD, num):
  #for i in range(len(lowerS)):
    currWindShear = windShear(lowerS, lowerD, upperS, upperD) #Calculate wind shear
    locNShear = np.array([])
    locNShear = np.append(locNShear, currWindShear) #[x Shear, y Shear]
    #locNShear = np.append(locNShear, coords[0]) #[x Shear, y Shear, lat, long]
    vectorMap[num] = locNShear #Replace 0s with [x Shear, y Shear, lat, long]
    #locationMap(num)

def locationMap(loc):
  plt.figure(figsize=(10, 7))
  if np.linalg.norm(np.array([vectorMap[loc][0], vectorMap[loc][1]])) != 0: #If magnitude not 0
    plt.arrow(vectorMap[loc][2], vectorMap[loc][3], vectorMap[loc][0], vectorMap[loc][1], width = .5)
    #plt.savefig(fname=f'/content/drive/MyDrive/Non-CAT Dataset/{loc}.png')

def computeVector():
  dir = []
  mag = []

  for i in range(len(windshear)):
    dir.append(round((np.arctan(windshear['Y'][i] / windshear['X'][i])) * 180 / math.pi, 2))
    mag.append(round(math.sqrt(math.pow(windshear['X'][i], 2) + math.pow(windshear['Y'][i], 2)), 2))

  return [mag, dir]

def findVector(length, lowerS, lowerD, upperS, upperD):
  global vectorMap, windshear
  vectorMap = np.zeros([length, 2])
  for num in range(0, length):
    dataArray(lowerS[num], lowerD[num], upperS[num], upperD[num], num)
  windshear = pd.DataFrame(vectorMap)
  windshear.columns = ['X', 'Y']
  mag_dir = computeVector()
  vectorMap = np.swapaxes(vectorMap, 0, 1)
  deltaS = abs(np.array(lowerS_arr) - np.array(upperS_arr)) #Absolute difference between wind speed (knots)
  deltaD = abs(np.array(lowerD_arr) - np.array(upperD_arr)) #Absolute difference between wind direction (degrees)
  data = pd.DataFrame({"DeltaS": deltaS, "DeltaD": deltaD, "X": vectorMap[0], "Y": vectorMap[1], "Magnitude": mag_dir[0], "Direction": mag_dir[1]})
  return data
  #path = time + "_" + data_type + "_" + dimension + ".xlsx"
  #data.to_excel(path)

#Save data
data = findVector(len(lowerS_arr), lowerS_arr, lowerD_arr, upperS_arr, upperD_arr)
data.to_excel("New_NonCAT_Data.xlsx")