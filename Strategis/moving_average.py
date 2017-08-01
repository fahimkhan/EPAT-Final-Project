import pandas as pd


from backtest import Strategy, Portfolio



class MovingAverageStrategy(Strategy):
	def __init__(self,symbol,bars,sma_window,lma_window):
		self.symbol =symbol
		self.bars = bars
		self.sma_window = sma_window
		self.lma_window  = lma_window




if __name__ == "__main__":

	symbol = "SBIN"
	bars = pd.read_csv("../Data/"+symbol+"-EQ.csv",index_col='Date',names=['Date','Open','High','Low','Close','Volume'],skiprows=1) #skip additional row with unwanted header name

	print bars.head()







