import xlwt
import requests
from bs4 import BeautifulSoup
import mechanize 
import os
from datetime import datetime, date, timedelta
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY
import calendar


os.mkdir("...Desktop/Demo-Result") ##replace

## enter login details

browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.open("http://proa.accuweather.com/pro/past-months.asp?LocationID=1")
browser.select_form(nr = 0) 
browser.form["username"] = "REPLACE THIS"
browser.form["password"] = "REPLACE THIS"
browser.submit()

## data manipulation
for loc in range(1, 3): 

	# initialize date range
	day = 1
	d1 = date(1992, 1, 1) ##customize
	d2 = date(2019, 1, 1) ##customize
	delta = d2 - d1  

	# initialize excel file
	book = xlwt.Workbook(encoding ="utf-8")
	sheet = book.add_sheet("sheet", cell_overwrite_ok=True)
	headers = 
	["Obs.Date",
	 "Act.High",
	 "Act.Low",
	 "Act.Avg",
	 "Norm.High",
	 "Norm.Low",
	 "Norm.Avg.",
	 "Norm.Dept",
	 "Rec.High",
	 "Rec.Year",
	 "Rec.Low",
	 "Rec.Year",
	 "Precip.Amt",
	 "SnowAmt.",
	 "SnowGround",
	 "HeatDeg Day",
	 "CoolDeg Day"]

	split = ""
	dir = "...Desktop/Demo-Result/" ##replace
	
	for i in range(len(headers)):
		sheet.write(0, i, headers[i])

	months = [dt.strftime("%m") for dt in rrule(MONTHLY, dtstart=d1, until=d2)]
	years = range(d1.year, d2.year+1)
	
	carry = 0
	
	for year in years:	
		for month in months:
			browser.select_form(nr=1)						
			browser.form.set_all_readonly(False)				
			browser.form["locationID"] = str(loc) # select location
		
			month = str(month)
			
			year = str(year)
			
			if month[0] == "0":
				month = month[1]
							
			# select month and year		
			browser.form["month_select"] = [month.encode("utf-8").decode("utf-8") ]
			browser.form["year_select"] = [year.encode("utf-8").decode("utf-8")]                                                  
			browser.submit()
		
			# scrape data	
			soup = BeautifulSoup(browser.response().read(), features="html5lib")
			column = soup.find_all("div", class_ = "dataCol")
			big = soup.find_all("div", class_= "dataColBig")				
			title = soup.find_all("title")[0].text.split()		
			split = "".join(i.encode("utf-8") for i  in title[-2:])
			cols = [i.text.strip() for i in column]
			bigs =[i.text.strip() for i in big]
	
			# download data into Excel
			currentCarry = 0
			for i in range(len(cols)):
				if i//12 != 0:
					if i%12 == 0:
						sheet.write(carry + i//12 + 1, i%12, year+ "-" +  month + "-" + str(currentCarry+1))
						currentCarry += 1
					else:
						sheet.write(carry + i//12 + 1, i%12, cols[i])
				
			for i in range(len(bigs)):
				if i // 5 != 0:
					sheet.write(carry + i//5 + 1, i%5 + 12, bigs[i])
							
			carry += currentCarry	
			day += 1
			
	book.save(dir + "/" + split + ".xls")
