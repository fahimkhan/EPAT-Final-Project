
import pandas as pd
import numpy as np
import pickle

from backtest import BacktestBase
from portfolio import Portfolio


train_test_split_ratio  = 0.5

class MovingAverageStrategy(BacktestBase):
	def run(self,SMA1,SMA2,model_path):
		daily_returns = []
		msg = 'Running SMA strategy for %s |SMA1 =%d |SMA2 = %d |ftc = %f|ptc = %f'
		msg = msg%(self.ticker,SMA1,SMA2,self.ftc,self.ptc)
		self.position = 0
		self.amount = self.initial_amount
		self.trades = 0

		self.hmm_model = pickle.load(open(model_path, "rb"))


		#Data Preparation
		self.data_run = self.data.copy()
		self.data_run['SMA1'] = self.data_run['Close'].rolling(SMA1).mean()
		self.data_run['SMA2'] = self.data_run['Close'].rolling(SMA2).mean()
		self.data_run["Returns"] = self.data_run["Close"].pct_change() 
		self.data_run.dropna(inplace=True)


		##Split data into training and test data
		training_data_len = int(len(self.data_run)*train_test_split_ratio) ##TO get training data
		end_date = self.data_run.index[training_data_len]
		start_date = self.data_run.index[training_data_len+1]
		training_df = self.data_run[:end_date]
		test_df =  self.data_run[start_date:]

		#Running for test data only
		self.data_run = test_df
		

		# print self.data_run.head()

		########Signals
		Signals = pd.DataFrame(index=self.data_run.index)
		Signals["PnL"] = 0
		Signals["Trade"] = 0
		Signals["Units"] = 0
				
		for bar in range(0,len(self.data_run)):
			##Storing observable varibale.In our case it is daily returns.
			daily_returns.append(self.data_run['Returns'].ix[bar])

			regime = self.regime_detection(daily_returns)

			if self.position == 0:
				if regime == 1:
					pass
				else:
					if self.data_run['SMA1'].ix[bar] > self.data_run['SMA2'].ix[bar]:
						self.place_buy_order(bar,amount=self.amount) 
						self.position = 1 #Take Position
						Signals["Trade"].ix[bar] = 1
						Signals["Units"].ix[bar] = int(self.units)
					else:
						Signals["Trade"].ix[bar] = 0
					
			elif self.position == 1:
				if regime == 1:
					print "Sell Without condition"
					Signals["Units"].ix[bar] = int(self.units)
					self.place_sell_order(bar,units=self.units)
					self.position = 0   #Market nuetral
					Signals["Trade"].ix[bar] = -1
				else:
					if self.data_run['SMA1'].ix[bar] < self.data_run['SMA2'].ix[bar]:
						Signals["Units"].ix[bar] = int(self.units)
						self.place_sell_order(bar,units=self.units)
						self.position = 0   #Market nuetral
						Signals["Trade"].ix[bar] = -1
					else:
						Signals["Trade"].ix[bar] = 0

			
				
		
		##Squaring off if holds any stock without checking any condition
		if self.position == 1:
			Signals["Units"].ix[bar] = int(self.units)
			self.place_sell_order(bar,units=self.units)
			self.position = 0   #Market nuetral
			Signals["Trade"].ix[bar] = -1


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
			
		self.trade_stats(bar,self.final_dataframe)

	def regime_detection(self,daily_returns):
		#Converting daily return list to numpy array
		daily_returns = np.column_stack([np.array(daily_returns)])
		hidden_state = self.hmm_model.predict(daily_returns)[-1]
		return hidden_state



if __name__ == "__main__":
	tickerList = ["HDFCBANK","ICICIBANK"]#,"KOTAKBANK","ONGC","INFY","RELIANCE","HDFC","LT","IOC","SBIN","HINDUNILVR",
	# "MARUTI","ITC","TCS"]

	initial_investement_amount = 10000

	for ticker in tickerList:
		model_path = "../Models/hmm_model_"+ticker+".pkl"
		sma = MovingAverageStrategy(ticker,initial_investement_amount)
		sma.run(50,250,model_path)


	portOBJ = Portfolio()
	portOBJ.show_portfolio_details()

	



	







