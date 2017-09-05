

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

    def show_portfolio_details(self):
    	print "Show portfolio"
    	print self.portfolio_details
