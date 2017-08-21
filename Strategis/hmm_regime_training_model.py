
import warnings
import pandas as pd
import datetime
import numpy as np
import pickle

from matplotlib import cm, pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator
import seaborn as sns
from hmmlearn.hmm import GaussianHMM

data_location = "../Data/IntraDay/"



def plot_in_sample_hidden_states(hmm_model, df):
	# Predict the hidden states array
	global returns
	hidden_states = hmm_model.predict(returns)
	# Create the correctly formatted plot
	fig, axs = plt.subplots(hmm_model.n_components,sharex=True, sharey=True)
	colours = cm.rainbow(np.linspace(0, 1, hmm_model.n_components))

	for i, (ax, colour) in enumerate(zip(axs, colours)):
		mask = hidden_states == i
		ax.plot_date(df.index[mask],df["Close"][mask],".", linestyle='none',c=colour)
		ax.set_title("Hidden State #%s" % i)
		ax.xaxis.set_major_locator(YearLocator())
		ax.xaxis.set_minor_locator(MonthLocator())
		ax.grid(True)
		plt.show()


if __name__ == "__main__":
	# Hides deprecation warnings for sklearn
	#warnings.filterwarnings("ignore")
	tickerList = ["HDFCBANK","ICICIBANK","KOTAKBANK","ONGC","INFY","RELIANCE",
	"HDFC","LT","IOC","SBIN","HINDUNILVR","MARUTI","ITC","TCS"]

	for ticker in tickerList:
		model_path = "../Models/hmm_model_"+ticker+".pkl"
		data = pd.read_csv(data_location+ticker+"-EQ.csv",index_col='Date',names=['Date','Open','High','Low','Close','Volume'],skiprows=1) 
		data["Returns"] = data["Close"].pct_change()
		data.dropna(inplace=True)
		data =  data.iloc[::-1]   ###Reverseas data is in descending order
		training_data_len = int(len(data)*0.70) ##TO get training data
		end_date = data.index[training_data_len]
		start_date = data.index[training_data_len+1]
		training_df = data[:end_date]
		test_df =  data[start_date:]
		# print training_df.tail()
		# print test_df.head()
		global returns
		returns = np.column_stack([training_df["Returns"]])
		# Create the Gaussian Hidden markov Model and fit it
		# to the returns cloumns fo training data, outputting a score
		hmm_model = GaussianHMM(n_components=2, covariance_type="full", n_iter=1000).fit(returns)
		print "Model Score:", hmm_model.score(returns)
		pickle.dump(hmm_model, open(model_path, "wb"))

