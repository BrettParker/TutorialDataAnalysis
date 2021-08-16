import glob
import pandas as pd
import matplotlib.pyplot as plt
from plotnine import ggplot, geom_boxplot, aes, geom_point, labs, geom_bar, coord_polar # ggplot for python, creates pretty graphs
import geopandas as gpd # GIS https://geopandas.org/docs/user_guide

countriesDat = list() # read csv's into a list
info = [] # so we know which csv's are in the list

for i in glob.glob("/Users/s5001793/Documents/SWC/python/extra_practice/assets/files/*gapminder.csv"):
    countriesDat.append(pd.read_csv(i))
    info.append(i)

countriesDat

for i in range(0,len(countriesDat)):
    countriesDat[i].set_index('country', inplace=True) # make country column the index 
    countriesDat[i] = countriesDat[i].loc[:,:"2020"] # subset the datasets to get country names and the years between 1800 and 2020

countriesDat

#life expentancy
countriesDat[0].describe()
#GDP
countriesDat[1].describe()

medLE = countriesDat[0].median(axis=0) 
medGDP = countriesDat[1].median(axis=0)


plt.scatter(medLE,medGDP)
plt.xlabel('Life Expectancy')
plt.ylabel('GDP')
plt.show()

gdp_index = pd.DataFrame(columns = countriesDat[1].columns, index = countriesDat[1].index)

for i in range(0,countriesDat[1].shape[1],1): # loop through each year 
    gdp_ = [] # create an empty list
    col = str(1800+i) # create a year variable that inceases with each loop, it will be used in sort_value on the next line
    gdp_ = pd.DataFrame(countriesDat[1].loc[:,col]) # subset year i
    range_value = gdp_.max() - gdp_.min() # get range for year i
    for j in range(0,countriesDat[1].shape[0],1): # loop through each country for year i
        gdp_.iloc[j,:] = (gdp_.iloc[j,:] - gdp_.min()) / range_value # for year i rescale country j between 0 (poorest) and 1 (richest)
    gdp_index.loc[:,col] = gdp_ # add the rescaled year i to the new df 

gdp_index

gdp_index['cumulative'] = gdp_index.sum(axis=1)
gdp_index['cumulative'] = (gdp_index['cumulative'] - gdp_index['cumulative'].min()) / (gdp_index['cumulative'].max() - gdp_index['cumulative'].min())    


plt.pie(gdp_index['cumulative'], labels=gdp_index.index)
plt.title("Countries cumulative GDP 1800-2020")

# add a circle at the center to transform it in a donut chart
my_circle=plt.Circle( (0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.show()

plt.bar(gdp_index.index, gdp_index['cumulative'])
plt.xticks(rotation=45)
plt.xlabel('Country')
plt.ylabel('Indexed cumulative GDP')
plt.title("Countries cumulative GDP 1800-2020")
plt.tight_layout()
plt.show()

regions = pd.read_csv("/Users/s5001793/Documents/SWC/python/extra_practice/assets/files/regions.csv")

regions.columns # we need to change the name Country to country in the regions dataframe. We can merge this with the index 'country' in gdp_index
regions.columns = ['country','regions']
gdp_index = pd.merge(gdp_index, regions, on=['country'])

plt.bar(gdp_index['regions'], gdp_index['cumulative'])
plt.xticks(rotation=45)
plt.xlabel('Region')
plt.ylabel('Indexed cumulative GDP')
plt.title("Regions cumulative GDP 1800-2020")
plt.tight_layout()
plt.show()




world = gpd.read_file("/Users/s5001793/Documents/SWC/python/extra_practice/assets/files/world/TM_WORLD_BORDERS-0.3.shp")

world.columns  # get the column names. we will need to change NAME to country so that we can merge columns from gpd_index onto it.
world['NAME'] # lets check that NAME is country names. yep it is
world.rename(columns={"NAME":"country"}, inplace=True)
world = world.merge(gdp_index, on='country')
# we will also plot the regions. to do this we will need to disolve the regions so that we have an outline for each region
world_regions = world.dissolve(by='REGION')

world.plot(column='cumulative',cmap='inferno',legend=True,legend_kwds={'label': "Countries cumulative GDP 1800-2020",'orientation': "horizontal"}) # https://matplotlib.org/stable/tutorials/colors/colormaps.html to find cmaps (i.e. colour maps)

from shapely.ops import cascaded_union

world.plot(column='REGION',facecolor="none")
plt.show()