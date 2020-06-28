# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 18:01:29 2020

@author: Johannes
"""

import requests
import re
import bs4
import pandas as pd

def parseContentsStr(element):
    # returns the contents of the tag and child-tags.
    content = ''
    for s in element.strings:
        content += s
    return content.rstrip()
    

html_source = requests.get('https://de.wikipedia.org/w/index.php?title=Liste_von_Kunstwerken_im_%C3%B6ffentlichen_Raum_in_Freiburg_im_Breisgau&stable=0&redirect=no').text

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

# drop the last table, it only contains unsorted sculptures, mostly without GPS
# coordinates ...
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
        for jdx, rd in enumerate(row):
            if columnNames[jdx] == 'Koordinate':
                # here we actually extract the coordinates from the html.
                m = re.search("params=(\d{1,3}\.\d*)_(\w)_(\d{1,3}\.\d*)_(\w)_", str(rd))
                rowData.append(parseContentsStr(rd))
            else:
                rowData.append(parseContentsStr(rd))
        df[idx].loc[len(df[idx])] = rowData

