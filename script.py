import glob
import pandas as pd



countriesDat = list() # read csv's into a list
info = [] # so we know which csv's are in the list

# read the csv's into a list in python 
for i in glob.glob("/Users/s5001793/Documents/SWC/python/extra_practice/assets/files/*csv"):
    countriesDat.append(pd.read_csv(i))
    info.append(i)

indexNames = []

for i in range(0,len(countriesDat)):
    for j in range(0, countriesDat[i].shape[0]):
        indexNames[j] = countriesDat[i].loc[:,:"country"]
        indexNames[j] = indexNames[j].strip(["(",",)"])
        countriesDat[i].index = indexNames[j]

for i in range(0,len(countriesDat)):
    countriesDat[i] = countriesDat[i].loc[:,"1800":"2020"]