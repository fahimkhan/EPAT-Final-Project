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
		self.data_run['SMA1'] = self.data_run['Close'].rolling(SMA1).mean()
		self.data_run['SMA2'] = self.data_run['Close'].rolling(SMA2).mean()
		self.data_run.dropna(inplace=True)

		########Signals
		Signals = pd.DataFrame(index=self.data_run.index)
		Signals["PnL"] = 0
		Signals["Trade"] = 0
		Signals["Units"] = 0
				
		for bar in range(0,len(self.data_run)):
			if self.position == 0:
				if self.data_run['SMA1'].ix[bar] > self.data_run['SMA2'].ix[bar]:
					self.place_buy_order(bar,amount=self.amount) 
					self.position = 1 #Take Position
					Signals["Trade"].ix[bar] = 1
					Signals["Units"].ix[bar] = int(self.units)
				else:
					Signals["Trade"].ix[bar] = 0
					
			elif self.position == 1:
				if self.data_run['SMA1'].ix[bar] < self.data_run['SMA2'].ix[bar]:
					Signals["Units"].ix[bar] = int(self.units)
					self.place_sell_order(bar,units=self.units)
					self.position = 0   #Market nuetral
					Signals["Trade"].ix[bar] = -1
				else:
					Signals["Trade"].ix[bar] = 0
				
			
		##Concatenating both dataframe
		frames = [self.data_run,Signals]
		self.final_dataframe = pd.concat(frames,axis=1, join_axes=[self.data_run.index])
		
		
		##PnL
		price=0.
		for bar in range(0,len(self.final_dataframe)):
			if self.final_dataframe['Trade'][bar] == 1:
				price = self.get_trade_price(bar,self.final_dataframe['Units'][bar])
			elif self.final_dataframe['Trade'][bar] == -1:
				self.final_dataframe['PnL'].ix[bar] = self.get_trade_price(bar,self.final_dataframe['Units'][bar]) - price
			# print "PnL Col" ,self.final_dataframe['PnL'].ix[bar]
		self.trade_stats(bar,self.final_dataframe)


symbolList = ["HDFCBANK"]#,"ICICIBANK","KOTAKBANK","ONGC","INFY","RELIANCE","HDFC","LT","IOC","SBIN","HINDUNILVR",
# "MARUTI","ITC","TCS"]

for symbol in symbolList:
	sma = MovingAverageStrategy(str(symbol),10000)
	sma.run(50,250)




	







