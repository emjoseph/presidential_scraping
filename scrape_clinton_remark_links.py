import requests
import json
from bs4 import BeautifulSoup as bs
import html
import time

# Array to store all the lainks to Trump's remarks
clinton_remarks = []
clinton_remark_urls = [
    "https://clintonwhitehouse6.archives.gov/1998/10/",
    "https://clintonwhitehouse6.archives.gov/1998/11/",
    "https://clintonwhitehouse6.archives.gov/1998/12/",
    "https://clintonwhitehouse6.archives.gov/1999/01/",
    "https://clintonwhitehouse6.archives.gov/1999/02/"]

def getThreeLetterMonthStringForMonthNumber(month_no):
    if month_no == 1:
        return "Jan"
    elif month_no == 2:
        return "Feb"
    elif month_no == 3:
        return "Mar"
    elif month_no == 4:
        return "Apr"
    elif month_no == 5:
        return "May"
    elif month_no == 6:
        return "Jun"
    elif month_no == 7:
        return "Jul"
    elif month_no == 8:
        return "Aug"
    elif month_no == 9:
        return "Sep"
    elif month_no == 10:
        return "Oct"
    elif month_no == 11:
        return "Nov"
    else:
        return "Dec"

def getClintonRemarksForUrl(url):
    global trump_remarks
    r = requests.get(url)
    soup = bs(r.text, "lxml")

    statements = soup.select('a')

    for i in range(0, len(statements)):
        statement_link = statements[i]['href']
        statement_link_parts = statement_link.split('-')

        # Build date string
        statement_date_year = statement_link_parts[0]
        statement_date_month = statement_link_parts[1]
        statement_date_day = int(statement_link_parts[2])
        statement_date_string = f"{getThreeLetterMonthStringForMonthNumber(int(statement_date_month))} {statement_date_day}, {statement_date_year}"

        # Build statement title
        statement_title = ""
        for i in range(3, len(statement_link_parts)):
            word = statement_link_parts[i]
            if word.lower() not in ["and", "by", "at", "to", "the", "on"] or i == 3:
                word = word.capitalize()
            statement_title += word
            statement_title += " "
            if i == len(statement_link_parts) - 1:
                statement_title = statement_title.replace(".html ", "")

        statement = {
            "title":statement_title,
            "link":"https://clintonwhitehouse6.archives.gov/"+f"{statement_date_year}/{statement_date_month}/"+statement_link,
            "time":statement_date_string
        }

        clinton_remarks.append(statement)

# Loop through all of the relevant clinton remark url pages
for i in range(len(clinton_remark_urls)):
    getClintonRemarksForUrl(clinton_remark_urls[i])
    print(f"Scrape {i+1} page of Clinton's remarks")
    time.sleep(0.15)

# Save all remarks to json file
with open('clinton_remarks.json', 'w') as file:
    json.dump(clinton_remarks, file, indent=4, ensure_ascii=True)


