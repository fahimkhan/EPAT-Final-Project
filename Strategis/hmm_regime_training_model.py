
import warnings
import pandas as pd
import datetime
import numpy as np
import pickle
from hmmlearn.hmm import GaussianHMM

data_location = "../Data/IntraDay/"
train_test_split_ratio  = 0.5


# Hides deprecation warnings for sklearn
warnings.filterwarnings("ignore")
tickerList = ["HDFCBANK","ICICIBANK","KOTAKBANK","ONGC","INFY","RELIANCE","HDFC","LT","IOC","SBIN","HINDUNILVR","MARUTI","ITC","TCS"]

for ticker in tickerList:
	model_path = "../Models/hmm_model_"+ticker+".pkl"
	data = pd.read_csv(data_location+ticker+"-EQ.csv",index_col='Date',names=['Date','Open','High','Low','Close','Volume'],skiprows=1) 
	data["Returns"] = data["Close"].pct_change() 
	data.dropna(inplace=True)
	#Reverse data to get proper ascending order
	data =  data.iloc[::-1]   
	
	##Split data into training and test data
	training_data_len = int(len(data)*train_test_split_ratio) ##TO get training data
	end_date = data.index[training_data_len]
	start_date = data.index[training_data_len+1]
	training_df = data[:end_date]
	test_df =  data[start_date:]
	# print training_df.tail()
	# print test_df.head()
	
	##Observable valriable on which hmm model will fits
	returns = np.column_stack([training_df["Returns"]])
	
	# Create the Gaussian Hidden markov Model and fit it
	# to the returns cloumns fo training data, outputting a score
	hmm_model = GaussianHMM(n_components=2, covariance_type="full", n_iter=1000).fit(returns)
	
	#Dump model in a file to use it later on
	pickle.dump(hmm_model, open(model_path, "wb"))

