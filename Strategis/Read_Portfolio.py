import pandas as pd

port_without_hmm = pd.read_pickle("port_without.pkl")
port_with_hmm = pd.read_pickle("port_with.pkl")


print "#######Portfolio Wihtout using HMM##########"
print port_without_hmm




print "###############Portfolio with using HMM############"
print port_with_hmm
