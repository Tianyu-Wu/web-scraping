# COLLECT SUBLET INFORMATION FROM WOKO.CH

# IMPORT LIBRARIES
from bs4 import BeautifulSoup as soup
from urllib import request
import csv
import time

# get the page and
home = "http://www.woko.ch"
url = "http://www.woko.ch/en/untermieter-gesucht"
page = request.urlopen(url)
scrap = soup(page,'html.parser')

# find result rows for region Zurich
zurich = scrap.find('div',{'id':'GruppeID_98'})
items = zurich.find_all('div',{'class':'inserat'})

# set titles
rows = []
row = ['Title','PostedTime','Duration','Address','Rent (CHF/Month)','Link','Room Info']
rows.append(row)

# loop through items and get info for each one
for item in items:
	header = item.find('div',{'class':'titel'})
	title = header.find('h3').getText().replace('ä','ae').replace('ö','oe').replace('ü','ue')
	postedtime = header.find('span').getText()
	link = home+item.find('a').get('href')
	data = item.find_all('td')
	duration = data[1].getText().strip('as from ').strip().replace('until','-')
	address = data[3].getText().replace('ä','ae').replace('ö','oe').replace('ü','ue')
	rent = item.find('div',{'class':'preis'}).getText().replace('.--','')
	detailpage = soup(request.urlopen(link),'html.parser')
	roominfo = home+detailpage.find('a',{'class':'btn btn-primary'}).get('href')
	rows.append([title,postedtime,duration,address,rent,link,roominfo])

# output to csv file
date = time.strftime("%m%d",time.localtime())
filename = "sublet_info_"+date+".csv"
with open(filename,"w",newline = "",encoding="utf-8") as output:
	writer = csv.writer(output)
	writer.writerows(rows)

print("finished scrapying "+filename)


