from nsepy import get_history
from datetime import date
import os
import time

location = "Data/Daily"

##Get the llist of ticker
with open("SecurityList") as f:
	tickers = f.readlines()
	


tickerList = [x.strip("\n") for x in tickers]
tickerList = filter(bool, tickerList)


for ticker in tickerList:
	dataframe = get_history(symbol=ticker,start=date(2005,1,1),end=date(2017,1,1),index=True)
	dataframe.to_csv(os.path.join(location,ticker)+"-EQ.csv",sep=",")
	

