def get_page_url(page, url):
    global n, total_pages
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(".js-restaurant__list_item")
    print("Page " + str(page) + " has " + str(len(items)) + " restaurants.")
    for item in items:
        n+=1
        print("n=", n)
        item_url = item.select("a")[1]['href']
        site_url = root_url + item_url
        showsite(site_url)
        if n == 1:
            number = soup.select("h1")[0]
            number_of_items = re.search(r'[0-9]+ Restaurants', number.text)
            number_of_items = int(re.search(r'[0-9]+', number_of_items.group()).group())
            total_pages = math.ceil(number_of_items/40)


def showsite(site_url):
    html = requests.get(site_url).text
    soup = BeautifulSoup(html, "html.parser")
    name = soup.select("h2")[0].text.strip()
    P_K = soup.select(".restaurant-details__heading-price")[0].text.strip()
    P_K = re.sub(r'\s+', ' ', P_K)
    P_K = P_K.split(" • ")
    address = soup.select(".restaurant-details__heading--list li")[0].text
    phone = soup.select(".flex-fill")[1].text
    information = soup.select(".js-show-description-text")[0].text.strip()
    image = soup.select(".masthead__gallery-image-item noscript img")[0]["src"].strip()
    try:
        time_hour = soup.select(".open__time-hour")[0].text.strip()
    except:
        time_hour = "NA"
    list_data = [name, P_K[1], P_K[0], information, address, site_url, phone, time_hour, image]
    list1.append(list_data)


def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scopes)
    return gspread.authorize(credentials)

import math
import re
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep


list1 = []
list_title = ["Name", "Style", "Price", "Information", "Address", "Website", "Phone", "Open Time", "Picture"]
list1.append(list_title)
n = 0
home_url = "https://guide.michelin.com/th/en/restaurants"
root_url = "https://guide.michelin.com"
get_page_url(1, home_url)

for page in range(2, total_pages+1):
    url = home_url+"/page/"+str(page)
    get_page_url(page, url)

auth_json_path = input("Enter your .json file name")
spreadsheet_key = input("Enter your spreadsheet_key")

gss_scopes = ['https://spreadsheets.google.com/feeds']
gss_clients = auth_gss_client(auth_json_path, gss_scopes)

sheet = gss_clients.open_by_key(spreadsheet_key).sheet1
sheet.clear()

for item in list1:
    sheet.append_row(item)
    sleep(1)

