import requests
import json
from bs4 import BeautifulSoup as bs
import html
import time

# Array to store all the lainks to Trump's remarks
clinton_remarks = []

def getRemarksForUrl(url):
    global clinton_remarks
    r = requests.get(url)
    soup = bs(r.text, "lxml")

    dates = []
    date_elements = soup.select('.views-field-field-docs-start-date-time-value.text-nowrap')
    for x in range(len(date_elements),0,-1):
        dates.append(date_elements[x-1].get_text().strip())

    titles = []
    links = []
    title_elements = soup.select('.views-field-title a')
    for y in range(len(title_elements),0,-1):
        title = title_elements[y-1].get_text().strip()
        titles.append(title)

        link = "https://www.presidency.ucsb.edu"+title_elements[y-1]['href'].strip()
        links.append(link)


    for z in range(len(title_elements),0,-1):
        remark = {
            "title": titles[z-1],
            "link": links[z-1],
            "time": dates[z-1],
        }
        clinton_remarks.append(remark)

# Loop through all of the remark pages on https://www.whitehouse.gov
for i in range(0, 26):
    url = f"https://www.presidency.ucsb.edu/advanced-search?field-keywords=&field-keywords2=&field-keywords3=&from%5Bdate%5D=10-08-1998&to%5Bdate%5D=02-12-1999&person2=200298&items_per_page=25&page={i}"
    getRemarksForUrl(url)
    print(f"Scrape {i} page(s) of Clinton's remarks")
    time.sleep(0.1)

# Save all remarks to json file
with open('clinton_remarks.json', 'w') as file:
    json.dump(clinton_remarks, file, indent=4, ensure_ascii=True)


