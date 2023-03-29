from selenium import webdriver
from datetime import datetime
import pandas as pd
import time

PATH = "C:\webdrivers\chromedriver.exe"
site = 'https://coinmarketcap.com/'

# create a DataFrame from csv and convert it to a dictionary
df0 = pd.read_csv('master.csv', index_col=0)
master_dict = df0.to_dict()

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M")

# Argument options for Driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--log-level=3")

# Initialize driver and get site url
driver = webdriver.Chrome(PATH, options=options)
driver.get(site)

# Scroll page 1000 units at a time to load JavaScript
page_position = 1000
for timer in range(0, 10):
    driver.execute_script("window.scrollTo(0, " + str(page_position) + ")")
    page_position += 1000
    time.sleep(2)

# Reads html into a DataFrame
html = driver.page_source
df = pd.read_html(html)[0][['Name', 'Price']]

driver.close()

# converts DataFrame to list for cleaning
source_list = df.values.tolist()

# loops through list to clean data and add to master_dict
for index, row in enumerate(source_list, start=1):
    # data cleaning for name and price
    raw_name = row[0]
    split_name = raw_name.split(f'{index}')
    formatted_name_ticker = split_name[0] + \
        " " + split_name[1].removesuffix('Buy')
    formatted_price = row[1].strip('"$').replace(',', '')

    # updates master_dict
    if formatted_name_ticker in master_dict.keys():
        master_dict[formatted_name_ticker][dt_string] = formatted_price
    else:
        master_dict[formatted_name_ticker] = {dt_string: formatted_price}

# Creates a FINAL DataFrame to store csv
df2 = pd.DataFrame.from_dict(master_dict)
df2.to_csv('master.csv')
