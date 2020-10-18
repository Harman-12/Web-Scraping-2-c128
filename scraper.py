from bs4 import BeautifulSoup
import requests
import time
import csv
import urllib3
urllib3.disable_warnings()

START_URL = "https://www.windows2universe.org/our_solar_system/moons_table.html"
headers = ["name", "year_discovered", "discoverer", "distance_from_planet(km)", "diameter(km)", "orbital_period", "host_planet"]
moons_data = []
page = requests.get(START_URL, verify=False)

def scrape_table(table):
    table_on = table.find_all("tr", attrs={"align": "left", "valign": "top"})[0]
    table_on = str(table_on.find_all("strong")[0]).replace("\r", " ").split(" ")[0].split(">")[1]
    for tr_tag in table.find_all("tr", attrs={"align": "center", "valign": "center"}):
        temp_list = []
        for index, td_tag in enumerate(tr_tag.find_all("td")):
            if index == 0:
                try:
                    temp_list.append(
                        td_tag.find_all("a")[0].contents[0]
                    )
                except:
                    try:
                        temp_list.append(td_tag.find_all("strong")[0].contents[0])
                    except:
                        temp_list.append(td_tag.contents[0])
            else:
                temp_list.append(td_tag.contents[0])
        temp_list.append(table_on)
        moons_data.append(temp_list)

soup = BeautifulSoup(page.content, "html.parser")
for index, table in enumerate(soup.find_all("table", attrs={"border": "5"})):
    if index == 0:
        continue
    else:
        scrape_table(table)

with open("moons.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(moons_data)
