import pandas as pd
import numpy as np

from backtest import BacktestBase


class MovingAverageStrategy(BacktestBase):
	def run(self,SMA1,SMA2):
		msg = 'Running SMA strategy for %s |SMA1 =%d |SMA2 = %d |ftc = %f|ptc = %f'
		msg = msg%(self.symbol,SMA1,SMA2,self.ftc,self.ptc)
		#print(msg)
		#print(50 * '=')
		#Re initialization
		self.position = 0
		self.amount = self.initial_amount
		self.trades = 0

		#Data Preparation
		self.data_run = self.data.copy()
		self.data_run['SMA1'] = self.data_run['Close'].rolling(SMA1).mean()
		self.data_run['SMA2'] = self.data_run['Close'].rolling(SMA2).mean()
		self.data_run.dropna(inplace=True)

		for bar in range(len(self.data_run)):
			if self.position == 0:
				if self.data_run['SMA1'].ix[bar] > self.data_run['SMA2'].ix[bar]:
					self.place_buy_order(bar,amount=self.amount) #Check for ftc and ptc ?
					self.position = 1 #Take Position
			elif self.position == 1:
				if self.data_run['SMA1'].ix[bar] < self.data_run['SMA2'].ix[bar]:
					self.place_sell_order(bar,units=self.units)
					self.position = 0   #Market nuetral

		self.close_out(bar)




symbolList = ["HDFCBANK","ICICIBANK","KOTAKBANK","ONGC","INFY","RELIANCE","HDFC","LT","IOC","SBIN","HINDUNILVR",
"MARUTI","ITC","TCS"]

for symbol in symbolList:
	sma = MovingAverageStrategy(str(symbol),10000)
	sma.run(50,250)




	







