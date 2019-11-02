import requests
import json
from bs4 import BeautifulSoup as bs
import html
import time

def loadTextForRemarkLink(url):
    r = requests.get(url)
    soup = bs(r.text, "lxml")
    paragraphs = soup.select('.editor p')

    text = ""
    for i in range(len(paragraphs)):
        text += paragraphs[i].get_text()
        text += '\n'
    return text


with open('trump_remarks.json') as trump_remarks_file:
    trump_remarks = json.load(trump_remarks_file)

    print(f'{len(trump_remarks)} remarks by Trump to scrape...')

    for i in range(len(trump_remarks)):
        remark = trump_remarks[i]
        remark_text = loadTextForRemarkLink(remark['link'])
        trump_remarks[i]['text'] = remark_text

        with open('trump_remarks_w_text.json', 'w') as file:
            json.dump(trump_remarks, file, indent=4, ensure_ascii=True)

        print(f'Scraped text for {i+1} remark(s)')
        time.sleep(0.25)
