import xlwt
import requests
from bs4 import BeautifulSoup
import mechanize 
import os
from xlrd import open_workbook
from xlutils.copy import copy
import urllib2
import urllib
import eventlet
from eventlet.green import urllib2
 
## enter login details
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.open("http://proa.accuweather.com/pro/past-months.asp?LocationID=1")
browser.select_form(nr = 0) 
browser.form.set_all_readonly(False)
browser.form["username"] = "REPLACE"
browser.form["password"] = "REPLACE"
browser.submit()

def parse(n):

	## initialize Excel 
	if not os.path.exists("...Desktop/locations/locations" + str(n) + ".xls"):
		book = xlwt.Workbook(encoding ="utf-8")
		sheet = book.add_sheet("sheet")
		sheet.write(0,0, "location")
		sheet.write(0,1, "coordinates")
		sheet.write(0,2, "source")
		sheet.write(0,3, "locationID")
		book.save("/Users/macuser/Desktop/AccuWeather-Parse-master/locations/locations" + str(n) + ".xls")

	for l in range(500 * (n-1), 500 * n):
		
		try:
			## Access data input and output
			rb = open_workbook("...Desktop/locations/locations" + str(n) + ".xls")
			wb = copy(rb)
			s = wb.get_sheet(0)
			browser.open("http://proa.accuweather.com/pro/past-months.asp?LocationID=" + str(l))

			## Data Scraping
			soup = BeautifulSoup(browser.response().read(), features="html5lib")
			title = soup.find_all("title")[0].text.split("Months:")[1]
			locName = title.encode("utf-8")	
			rawlat = soup.find_all("div", class_= "textsmall")
			latlong = rawlat[0].text.encode("utf-8")
			sourceraw = soup.find_all("div", class_= "textmedred")[0].text.split()[-4:]
			source = " ".join(i.encode("utf-8") for i in sourceraw)

			s.write(l,0,locName)
			s.write(l,1, latlong)
			s.write(l,2, source)
			s.write(l,3, str(l))
			
			wb.save(".../Desktop/locations/locations" + str(n) + ".xls")
			
		except:
			pass
parse(1)
