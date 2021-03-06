# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 18:01:29 2020

@author: Johannes
"""

import requests
import bs4
import pandas as pd

def parseContentsStr(element):
    # returns the contents of the tag and child-tags.
    content = ''
    for s in element.strings:
        content += s.rstrip()
    return content
    

html_source = requests.get('https://de.wikipedia.org/wiki/Liste_von_Kunstwerken_im_%C3%B6ffentlichen_Raum_in_Freiburg_im_Breisgau').text

# html_source = html_source[:18000]

soup = bs4.BeautifulSoup(html_source, 'lxml')


# get the headers in the wiki-page 
headers = soup.find_all("span", "mw-headline")
# ignore last two entries 'Weblinks' and 'Einzelnachweise'
headers = headers[:-2]

areaNames = [];
for hh in headers:
    areaNames.append(parseContentsStr(hh))    

# get all the tables on the page
tables = soup.find_all("table", "wikitable")

# drop the last table, I dont know where it comes from...
tables = tables[:-1]

df = []
# parse all the area tables into pandas dataFrames
for idx, t in enumerate(tables):
    # get the name for the table columns
    headerBar = t.find_all("th")
    columnNames = []
    for hh in headerBar:
        columnNames.append(hh.contents[0].rstrip())
    
    # from this we create our dataFrame
    df.append(pd.DataFrame(columns=columnNames))
    
    # now that we have the header for the table, lets get the rows
    rows = t.find_all("tr")
    # for some reason the header reappears in rows, so we drop the first entry
    rows = rows[1:]
    for tr in rows:        
        row = tr.find_all("td")
        rowData = []
        for rd in row:
            rowData.append(parseContentsStr(rd))
        df[idx].loc[len(df[idx])] = rowData

