## creates scripts that collects 500 location data points each

## create separate scripts to download scraped data simultaneously on multiple Excel files

lines = []

with open(".../Desktop/locationScripts/l1.py") as f:
    lines = f.readlines()
    
## saves files in locationScripts directory
for n in range(1 , 3000/500):	 ##customize the range of script numbers
	with open(".../Desktop/locationScripts/l" + str(n) + ".py", "w+") as f:
		for i in range(0, len(lines) -1):
			f.write(lines[i])		
		f.write("parse(" + str(n) + ")")
		
