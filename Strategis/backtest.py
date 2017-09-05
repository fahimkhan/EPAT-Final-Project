
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
plt.style.use('seaborn')

from portfolio import Portfolio


data_location = "../Data/IntraDay/"

class FinancialData(object):
	"""docstring for FinancialData"""
	def __init__(self, ticker):
		self.ticker = ticker
		self.portfolioOBJ = Portfolio()
		self.get_data()

	def get_data(self):
		#skip additional row with unwanted header name
		self.data = pd.read_csv(data_location+self.ticker+"-EQ.csv",index_col='Date',names=['Date','Open','High','Low','Close','Volume'],skiprows=1) 
		#self.data = pd.read_csv(data_location+self.ticker+"-EQ.csv",index_col='Date',names=['Date','Symbol','Series',
		#	'Prev Close','Open','High','Low','Last','Close','VWAP','Volume','Turnover','Trades','Deliverable Volume','%Deliverble'],skiprows=1) 
		
		#Reverseas data to get it in ascending order
		self.data =  self.data.iloc[::-1]   

		


	def plot_data(self, cols=['Close']):
		self.data[cols].plot(figsize=(10, 6))
		plt.show()

class BacktestBase(FinancialData):
	# def __init__(self,ticker,start,end,amount,ftc=0.0,ptc=0.0):
	def __init__(self,ticker,amount,ftc=0.0,ptc=0.0):	
		FinancialData.__init__(self,ticker)
		### Use date if you want to backtest on range of date
		# self.start = start
		# self.end = end
		self.ftc = ftc
		self.ptc = ptc
		self.amount = amount
		self.initial_amount = amount
		self.units = 0
		self.trades = 0
		self.position = 0

	def print_balance(self,date=''):
		"""
		Printing Current Balance
		"""
		pass
		#print("%s |Current balance is %9.2f " %(date,self.amount))

	def get_trade_price(self,bar,units):
		date,price = self.get_date_price(bar)
		buy_amount = units*price
		txn_cost = self.get_txn_cost(buy_amount)
		trade_price =  buy_amount+txn_cost
		return trade_price

	def get_date_price(self,bar):
		"""
		Get date and price for current index data
		"""
		date = str(self.data_run.index[bar])[:10]
		price = self.data_run['Close'].ix[bar]
		return date,price

	def get_txn_cost(self,amount):
		"""
		Calculate Txn Cost
		"""
		rate = 0.0001
		txn_cost = rate*amount
		if txn_cost > 20:
			txn_cost = 20
		return txn_cost

	def get_trade_units(self,amount,price):
		"""
		Get Unit for trading based on amount available
		"""
		units = math.floor(amount/price)
		return units

	def place_buy_order(self,bar,units=None,amount=None):
		"""
		Placing buy order
		"""
		
		date,price = self.get_date_price(bar)  ##Current date and price of share
		amount = amount - self.get_txn_cost(amount) ##Make sure transaction amount is there for trading 

		##Getting  units
		if units is None:
			units = self.get_trade_units(amount,price) 

		
		buy_amount = units*price
		txn_cost = self.get_txn_cost(buy_amount)
		self.amount = self.amount - buy_amount - txn_cost
		self.units += units
		self.trades += 1
		
		# print "##########Buying#######################"
		# print "Buying Price################",str(price)
		# print "Transaction Cost#############",str(txn_cost)
		# print "Units Purchsed############",str(units)
		# print "Amount to deducted########",str(buy_amount-txn_cost)
		# print "Balance############",str(self.amount)
		
		#print("%s |Buying  %4d  units  at  %8.2f "%(date,units,price))
		#self.print_balance(date)

	def place_sell_order(self,bar,units=None,amount=None):
		"""
		Placing Sell Order
		"""
		
		date,price = self.get_date_price(bar)
		if units is None:
			units = math.floor(amount/price) 

		
		sell_amount = units*price
		txn_cost = self.get_txn_cost(sell_amount)
		self.amount = self.amount + sell_amount - txn_cost
		self.units -= units
		self.trades += 1
		#print("%s |Selling  %4d  units  at  %8.2f "%(date,units,price))
		# print "##########Selling#######################"
		# print "Selling Price################",str(price)
		# print "Units Sold############",str(units)
		# print "Transaction Cost#############",str(txn_cost)
		# print "Amount to added########",str(sell_amount-txn_cost)
		# print "Balance############",str(self.amount)
		self.print_balance(date)

	def trade_stats(self,bar,final_dataframe):
		"""
		Final status after backtesting like final balance,performance,sharpe ratio,max drawdawn etc
		"""
		pnl_data = final_dataframe['PnL'].cumsum()
		sharpe_ratio = np.sqrt(252) * (np.mean(final_dataframe['PnL'])) / np.std(final_dataframe['PnL'])
		performance = (self.amount-self.initial_amount)/self.initial_amount *100


		print "#############Start##############"
		print "Ticker :",self.ticker
		print "Initial Amount Invested : ",self.initial_amount
		print "Final Balance :",self.amount
		print "#Trades : %d"%self.trades
		print "Performance : ",performance
		print "PnL : ",final_dataframe['PnL'].sum()
 		print "Sharpe Ratio", "%0.2f" % sharpe_ratio
 		

 		##Add details to portfolio
 		port_details = [self.ticker,self.initial_amount,self.amount,self.trades,final_dataframe['PnL'].sum(),sharpe_ratio,performance]


 		self.portfolioOBJ.add_portfolio_details(port_details)

		###Maximum Drawdawn
		#pnl_data.plot(figsize=(10, 6))
		#plt.show()
		print "##############End#################"


# objFinancialData = FinancialData("SBIN")
# objFinancialData.plot_data()



