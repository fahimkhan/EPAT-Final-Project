
import warnings
import pandas as pd
import datetime


data_location = "../Data/IntraDay/"


if __name__ == "__main__":
	# Hides deprecation warnings for sklearn
	#warnings.filterwarnings("ignore")
	tickerList = ["HDFCBANK"]#,"ICICIBANK","KOTAKBANK","ONGC","INFY","RELIANCE","HDFC","LT","IOC","SBIN","HINDUNILVR",
	# "MARUTI","ITC","TCS"]

	for ticker in tickerList:
		model_path = "../Models/hmm_model_"+ticker+".pkl"
		data = pd.read_csv(data_location+ticker+"-EQ.csv",index_col='Date',names=['Date','Open','High','Low','Close','Volume'],skiprows=1) 
		data["Returns"] = data["Close"].pct_change()
		data.dropna(inplace=True)
		data =  data.iloc[::-1]   ###Reverseas data is in descending order
	# 	training_data_len = int(len(data)*0.70) ##TO get training data
	# 	end_date = data.index[training_data_len]
	# 	start_date = data.index[training_data_len+1]
	# 	training_df = data[:end_date]
	# 	test_df =  data[start_date:]
	# 