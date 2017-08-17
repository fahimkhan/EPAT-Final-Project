from nsepy import get_history
from datetime import date
import os
import time

location = "Data/Daily"

##Get the llist of ticker
with open("SecurityList") as f:
	tickers = f.readlines()
	


tickerList = [x.strip() for x in tickers]
tickerList = filter(bool, tickerList)

print tickerList
for ticker in tickerList:
	print ticker
	if ticker=="NIFTY":
		data = get_history(symbol=ticker,start=date(2000,1,1),end=date(2017,7,31),index=True)
	else:
		data = get_history(symbol=ticker,start=date(2000,1,1),end=date(2017,7,31))

	print data.head()
	data.to_csv(os.path.join(location,ticker)+"-EQ.csv",sep=",")




	time.sleep(20)
	

