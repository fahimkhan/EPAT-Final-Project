import pandas as pd
import numpy as np

from backtest import BacktestBase


class MovingAverageStrategy(BacktestBase):
	def run(self,SMA1,SMA2):
		msg = 'Running SMA strategy for %s |SMA1 =%d |SMA2 = %d |ftc = %f|ptc = %f'
		msg = msg%(self.symbol,SMA1,SMA2,self.ftc,self.ptc)
		self.position = 0
		self.amount = self.initial_amount
		self.trades = 0

		#Data Preparation
		self.data_run = self.data.copy()
		self.data_run['Trade'] = 'NaN'
		self.data_run['PnL'] = 0.
		self.data_run['SMA1'] = self.data_run['Close'].rolling(SMA1).mean()
		self.data_run['SMA2'] = self.data_run['Close'].rolling(SMA2).mean()
		self.data_run.dropna(inplace=True)

		
		for bar in range(len(self.data_run)):
			if self.position == 0:
				if self.data_run['SMA1'][bar] > self.data_run['SMA2'][bar]:
					self.place_buy_order(bar,amount=self.amount) #Check for ftc and ptc ?
					self.position = 1 #Take Position
					self.data_run['Trade'].loc[bar] = 1
				else:
					self.data_run['Trade'].loc[bar] = 0
			elif self.position == 1:
				if self.data_run['SMA1'][bar] < self.data_run['SMA2'][bar]:
					self.place_sell_order(bar,units=self.units)
					self.position = 0   #Market nuetral
					self.data_run['Trade'].loc[bar] = -1
				else:
					self.data_run['Trade'].loc[bar] = 0

		# ##Creating PNL column
		# price=0.
		# for bar in range(len(self.data_run)):
		# 	if self.data_run['Trade'][bar] == 1:
		# 		price = self.data_run['Close'][bar]*self.units
		# 	elif self.data_run['Trade'][bar] == -1:
		# 		self.data_run['PnL'][bar] = self.data_run['Close'][bar]*self.units - price
		# 	else:
		# 		self.data_run['PnL'][bar] = 0

		

		# self.close_out(bar)


symbolList = ["HDFCBANK"]#,"ICICIBANK","KOTAKBANK","ONGC","INFY","RELIANCE","HDFC","LT","IOC","SBIN","HINDUNILVR",
# "MARUTI","ITC","TCS"]

for symbol in symbolList:
	sma = MovingAverageStrategy(str(symbol),10000)
	sma.run(50,250)




	







