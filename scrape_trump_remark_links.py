import requests
import json
from bs4 import BeautifulSoup as bs
import html
import time

# Array to store all the lainks to Trump's remarks
trump_remarks = []

def getTrumpRemarksForUrl(url):
    global trump_remarks
    r = requests.get(url)
    soup = bs(r.text, "lxml")

    statements = soup.select('.briefing-statement__content')

    for i in range(0, len(statements)):
        remark_title = statements[i].select('a')[0].get_text().replace('\n', ' ').replace('\r', '').replace('\t',
                                                                                                            '').encode().decode()
        remark_type = None
        if len(statements[i].select('a')) > 1:
            remark_type = statements[i].select('a')[1].get_text().replace('\n', ' ').replace('\r', '').replace('\t', '')
        remark_link = statements[i].select('a')[0]['href'].replace('\n', ' ').replace('\r', '').replace('\t', '')
        remark_time = statements[i].select('time')[0].get_text().replace('\n', ' ').replace('\r', '').replace('\t', '')

        remark_time_month = remark_time.split(' ')[0]
        remark_time_day = int(remark_time.split(' ')[1].split(',')[0])

        if remark_time_month == 'Sep' and remark_time_day < 24:
            # Don't store archives before the impeachment inquiry
            continue

        remark = {
            "title": remark_title,
            "link": remark_link,
            "time": remark_time,
            "category": remark_type
        }
        trump_remarks.append(remark)

# Loop through all of the remark pages on https://www.whitehouse.gov
for i in range(1, 7):
    getTrumpRemarksForUrl(f'https://www.whitehouse.gov/remarks/page/{i}')
    print(f"Scrape {i} page(s) of Trump's remarks")
    time.sleep(0.1)

# Save all remarks to json file
with open('trump_remarks.json', 'w') as file:
    json.dump(trump_remarks, file, indent=4, ensure_ascii=True)


