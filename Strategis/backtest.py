
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn')



data_location = "../Data"

class FinancialData(object):
	"""docstring for FinancialData"""
	def __init__(self, symbol):
		self.symbol = symbol
		self.get_data()

	def get_data(self):
		#skip additional row with unwanted header name
		self.data = pd.read_csv("../Data/"+self.symbol+"-EQ.csv",index_col='Date',names=['Date','Open','High','Low','Close','Volume'],skiprows=1) 
	
	def plot_data(self, cols=['Close']):
		self.data[cols].plot(figsize=(10, 6))
		plt.show()



class BacktestBase(FinancialData):
	def __init__(self,symbol,start,end,amount,ftc=0.0,ptc=0.0):
		FinancialData.__init__(self,symbol)
		self.start = start
		self.end = end
		self.amount = amount
		self.initial_amount = amount
		self.ftc = ftc
		self.ptc = ptc
		self.units = 0
		self.trades = 0
		self.position = 0

	def print_balance(self,date=''):
		print("%s |Current balance is %9.2f " %(date,self.amount))

	def get_date_price(self,bar):
		date = str(self.run.index[bar])[:10]
		price = self.run['Close'].ix[bar]
		return date,price

	def place_buy_order(self,bar,units=None,amount=None):
		date,price = self.get_date_price(bar)
		if units is None:
			units = math.floor(amount/price) #include ftc and ptc

		self.amount -= (units*price)*(1+self.ptc)+self.ftc
		self.units += units
		self.trades += 1
		print("%s |Buying  %4d  units  at  %8.2f "%(date,units,price))
		self.print_balance(date)

	def place_sell_order(self,bar,units=None,amount=None):
		date,price = self.get_date_price(bar)
		if units is None:
			units = math.floor(amount/price) #include ftc and ptc

		self.amount += (units*price)*(1-self.ptc)-self.ftc
		self.units -= units
		self.trades += 1
		print("%s |Selling  %4d  units  at  %8.2f "%(date,units,price))
		self.print_balance(date)

	def close_out(self,bar):
		date,price = self.get_date_price(bar)
		self.amount += (self.units*price) #Include ftc and ptc ?
		print(50 * '=')
		print ("%s |buying/selling %d units at %7.2f"%(date,self.units,price))
		print("Final balance [$]: %8.2f"%self.amount)
		perf = (self.amount-self.initial_amount)/self.initial_amount *100
		print("Performace [%%]:%8.2f"%perf)
		print("#Trades :%d"%self.trades)




# objFinancialData = FinancialData("SBIN")
# objFinancialData.plot_data()



