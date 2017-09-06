
import numpy as np
import pandas as pd

class PortfolioHandler(type):
    instances = dict()

    def __call__(self, *args, **kwargs):
        if self.__name__ not in PortfolioHandler.instances:            
            PortfolioHandler.instances[self.__name__] = type.__call__(self, *args, **kwargs)
        return PortfolioHandler.instances[self.__name__]


class Portfolio(object):
    __metaclass__ = PortfolioHandler


    def __init__(self):
    	self.portfolio_details = [["","Invested Amount","Final Amount","Number of Trades","PnL","Sharpe Ratio","Performance"]]

    def add_portfolio_details(self,port_list):
    	print "Adding Portfolio"
    	self.portfolio_details.append(port_list)

    def show_portfolio_details(self,filename):
    	port_array = np.array(self.portfolio_details)
        port_df = pd.DataFrame(data=port_array[1:,1:],index=port_array[1:,0],columns=port_array[0,1:])
        port_df.to_pickle(filename)
        print port_df
        
