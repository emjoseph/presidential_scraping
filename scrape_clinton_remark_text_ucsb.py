import requests
import json
from bs4 import BeautifulSoup as bs
import html
import time
import re
def loadTextForRemarkLink(url):
    r = requests.get(url)
    soup = bs(r.text, "lxml")
    paragraphs = soup.select('.field-docs-content p')

    text = ""
    for i in range(len(paragraphs)):
        text += paragraphs[i].get_text().strip()
        text += '\n'
    return text

with open('clinton_remarks.json') as remarks_file:

    remarks = json.load(remarks_file)
    print(f'{len(remarks)} remarks to scrape...')

    for i in range(len(remarks)):
        remark = remarks[i]
        remark_text = loadTextForRemarkLink(remark['link'])
        remark_text = remark_text.replace('\n', ' ')
        remark_text = remark_text.replace('\r', ' ')
        remark_text = remark_text.strip()
        remark_text = re.sub(' +', ' ',remark_text)
        remarks[i]['text'] = remark_text

        with open('clinton_remarks_w_text.json', 'w') as file:
            json.dump(remarks, file, indent=4, ensure_ascii=True)

        print(f'Scraped text for {i+1} remark(s)')
        time.sleep(0.15)
