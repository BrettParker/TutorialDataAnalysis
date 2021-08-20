---
layout: default
---

Data analysis contains several skills. It can involve cleaning, subsetting, visualising the data to understand trends, and preforming statistics to quantify trends.
## Data for this class

<a href="./files/gdp.csv" target="_blank">GDP</a> <br>
<a href="./files/life_expectancy_years.csv" target="_blank">life expectancy</a> <br>
Gap minder data is also avaliable from: https://www.gapminder.org/data/ <br>

We will also use a regions datasets, which can be downloaded here: https://github.com/BrettParker/TutorialDataAnalysis/tree/master/assets/files/world. Please download all four files within that folder. This is a GIS dataset. <br>

## Read in the csv files

```python
import glob
import pandas as pd
import matplotlib.pyplot as plt
from plotnine import ggplot, geom_boxplot, aes, geom_point, labs, geom_bar, coord_polar # ggplot for python, creates pretty graphs
import geopandas as gpd # GIS https://geopandas.org/docs/user_guide
import scipy as sp 

countriesDat = list() # read csv's into a list
info = [] # so we know which csv's are in the list

for i in glob.glob("~/*gapminder.csv"):
    countriesDat.append(pd.read_csv(i))
    info.append(i)
```
The first dataset is life expentancy i.e. countriesDat[0] and the second is GDP i.e. countriesDat[1]

## Lets explore the data
```python
countriesDat
```
Let set the index to the column country

The year is projected to 2100, lets index it to 2020. Remember: iloc is for indexing by the number of the [column,row], while loc uses the labels.

```python
for i in range(0,len(countriesDat)):
    countriesDat[i].set_index('country', inplace=True) # make country column the index 
    countriesDat[i] = countriesDat[i].loc[:,:"2020"] # subset the datasets to get country names and the years between 1800 and 2020

countriesDat
```

Lets have a look at the yearly summary statistics for life expectancy and GDP across all countries.

```python
#life expentancy
desLE = countriesDat[0].describe()
desLE
#GDP
desGDP = countriesDat[1].describe()
desGDP
```

Mean GDP and mean life expectancy are increasing our time.
If you look at the min, max and mean for life expectancy, looks like they are all increasing, thats a good sign. But there looks like there is a big difference between the min and the max and a fair difference between the 25th and 75th quartiles. Furthermore, over time the min GDP barely increases while and max GDP increases masively. All these indicate inequality between countries.

Next lets explore between country inequality through visualisation.
We can get the means from the describe dataframe we created in the previous step. We will need to subset mean from each dataframe.
Plot using the matplotlib package.

```python
plt.plot(desLE.loc['mean'])
plt.plot(desLE.loc['25%'])
plt.plot(desLE.loc['75%'])
plt.ylabel('Life Expectancy')
plt.xlabel('Time (1800-2020)')
plt.show()
```
Looks like there is either some bad data, something going on with the huge negative spike in life expectency. WW1 or spanish flu???? Needs to be looked into. You can also see the effects of WW2 on life expectancy.
But you can clearly see the discrepancy between countries.

```python
plt.plot(desGDP.loc['mean'])
plt.plot(desGDP.loc['25%'])
plt.plot(desGDP.loc['75%'])
plt.ylabel('GDP')
plt.xlabel('Time (1800-2020)')
plt.show()
```

Well there is a massive between country inequality with GDP.

## Is life expectency correlated with GDP?
Lets see if the mean life expectency for all countries is correlated to the mean GDP for all countries.

```python
plt.scatter(desLE.loc['mean'],desGDP.loc['mean'])
plt.xlabel('Life Expectancy')
plt.ylabel('GDP')
plt.show()
```

Thats interesting, on average it looks like GDP is correlated with life expectancy. To a point of about $7000, then after this point life expectency slows with increasing GDP.

## What about rich vs poor countries?
Earlier on we used the describe function and visualisations, and found a large inequality in GDP between rich and poor countries, and to a lesser extent life expectancy.
Lets dive a bit deeper into that.

First we need to rank the countries from richest to poorest. We could rank them based on the most recent year (i.e. their GDP in 2020). However we will use the GDP's from all years so that we have the average richness of the country.

To do this we will first rescale each countries yearly GDP (all years from 1800 to 2020) based on the country with the highest and lowest GDP for that year. Effectively that will rank each country from richest to poorest for each year. 
Then for each country we can sum their year on year rank scores to get a single cumulative score based on all years. 
The final score will be a decimal score with richest as 1 and poorest as 0.

For more information about rescaling, have a look <a href='https://www.stackvidhya.com/how-to-normalize-data-between-0-and-1-range/' target='_blank'>here</a>

The recale function will need to be preformed on each year, for each country. This sounds like a loop problem.

```python
gdp_index = pd.DataFrame(columns = countriesDat[1].columns, index = countriesDat[1].index) # an empty dataframe to write the rescaled values to.
# We have provided dimensions, index and column names for the dataframe.
# countriesDat[1].columns and countriesDat[1].index, lists the column and index names of a dataframe respectively

for i in range(0,countriesDat[1].shape[1],1): # loop i through each year 
    gdp_ = [] # create an empty list to add the subset year i data too
    col = str(1800+i) # create a year variable that inceases with each loop, it will be used to subset each year on the next line
    gdp_ = pd.DataFrame(countriesDat[1].loc[:,col]) # subset year i
    range_value = gdp_.max() - gdp_.min() # get GDP range for year i
    for j in range(0,countriesDat[1].shape[0],1): # creat a new loop to loop through each country j for year i
        gdp_.iloc[j,:] = (gdp_.iloc[j,:] - gdp_.min()) / range_value # for year i rescale country j between 0 (poorest) and 1 (richest)
    gdp_index.loc[:,col] = gdp_ # add the rescaled year i to the new df 

gdp_index

gdp_index['cumulative'] = gdp_index.sum(axis=1) #create a new column called 'cumulative' and write the sum of all years per country
gdp_index['cumulative'] = (gdp_index['cumulative'] - gdp_index['cumulative'].min()) / (gdp_index['cumulative'].max() - gdp_index['cumulative'].min()) #rescale cumulative value
gdp_index.rename(columns={"cumulative":"GDPrank"}, inplace='True') #lets rename the cumulative column to GDP rank, tht makes more sense
```
Lets visualise the ranked data in an attempt to better identify differences between countries
Lets plot a barchart to show the indexed GDP per country.

```python

# Create a barchart
plt.bar(gdp_index.index, gdp_index['GDPrank'])
plt.xticks(rotation=45)
plt.xlabel('Country')
plt.ylabel('Indexed cumulative GDP')
plt.title("Countries cumulative GDP 1800-2020")
plt.tight_layout()
plt.show()
```
Ok, better, there are large differences between countries, but we cannot distinguish the individual countries. Lets group countries by region. We will need to download and read in the regions file, then merge the regions dataframe onto the our GDP and life expencancy dataframes.

```python
lowestLE = countriesDat[0].loc[gdp_index['GDPrank'].idxmin()] # idxmin gets the index position of the minimum value, i.e. a value that can be used to subset the dataset based on the lowest cumulative gdp
lowestGDP = countriesDat[1].loc[gdp_index['GDPrank'].idxmin()]

highestLE = countriesDat[0].loc[gdp_index['GDPrank'].idxmax()]
highestGDP = countriesDat[1].loc[gdp_index['GDPrank'].idxmax()]

dat = pd.DataFrame([lowestLE,lowestGDP,highestLE,highestGDP]).T
dat.columns = ['lowestLE','lowestGDP','highestLE','highestGDP']
```
Plot the GDP vs life expectancy for the lowest and for the highest ranked GDP countries.
```python
plt.scatter(dat['lowestLE'],dat['lowestGDP'], label="Poorest")
plt.scatter(dat['highestLE'],dat['highestGDP'], label="Richest")
plt.legend(loc="upper left")
plt.xlabel('Life Expectancy')
plt.ylabel('GDP')
plt.show()

```

Well that doesn't really add up. It doesn't really seem that life expectancy is correlated with GDP. If we look at the global average it seems that GDP and life expectancy are correlated. But if we look at the poorest country there is no correlation, life expectancy has increased, while GDP has remained virtually flat. 
There must be something else that is driving increasing global life expectancy. Happiness, access to medicine and hospitals, war???

