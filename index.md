---
layout: default
---

Data analysis contains several skills. It can involve cleaning, subsetting, visualising the data to understand trends, and preforming statistics to quantify trends.
## Data for this class

<a href="./files/gdp.csv" target="_blank">GDP</a> <br>
<a href="./files/life_expectancy_years.csv" target="_blank">life expectancy</a> <br>
Gap minder data is also avaliable from: https://www.gapminder.org/data/ <br>

<a href="./files/regions.csv" target="_blank">Regions</a> <br>

## Read in the csv files

```python
import glob
import pandas as pd
import matplotlib.pyplot as plt
from plotnine import ggplot, geom_boxplot, aes, geom_point, labs, geom_bar, coord_polar # ggplot for python, creates pretty graphs
import geopandas as gpd # GIS https://geopandas.org/docs/user_guide

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
countriesDat[0].describe()
#GDP
countriesDat[1].describe()
```
If you look at the min, max and mean for life expectancy, looks like they are all increasing, thats a good sign. But there looks like there is a big difference between the min and the max. There are some huge inequatities for GDP, the min barely increases while and max increases masively.

## Does GDP have anything to do with life expectency?
How can we see if GDP has an influence on life expectancy?

Lets see if the average GDP for all countries is correlated to the average life expectencies for all countries.
Lets get the medians.
```python
medLE = countriesDat[0].median(axis=0) 
medGDP = countriesDat[1].median(axis=0)
```
Plot them against each other using the matplotlib package
```python
plt.scatter(medLE,medGDP)
plt.xlabel('Life Expectancy')
plt.ylabel('GDP')
plt.show()
```

Well thats interesting, on average it looks like GDP is correlated with life expectancy. To a point of about $8000, then after this point life expectency does not increase along with GDP.

## What about rich vs poor countries?
We saw that there was large inequality in GDP between rich and poor countries, and to a lesser extent life expectancy.
Lets dive a bit deeper into that.
First we need to sort the countries from richest to poorest.
Lets rank the coutries from richest 1 to poorest 0. To do this we will first rescale each countries yearly GDP (1800-2020), then for each country we can sum their year on year rank scores to get a single cumulative score based on all years.

```python
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
```
Lets visualise this data in an attempt to better identify differences between countries

```python
# Create a pieplot
plt.pie(gdp_index['cumulative'], labels=gdp_index.index)
plt.title("Countries cumulative GDP 1800-2020")

# add a circle at the center to transform it in a donut chart
my_circle=plt.Circle( (0,0), 0.7, color='white')
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.show()

```
Well that is impossible to understand, lets plot some barcharts.

```python

# Create a barchart
plt.bar(gdp_index.index, gdp_index['cumulative'])
plt.xticks(rotation=45)
plt.xlabel('Country')
plt.ylabel('Indexed cumulative GDP')
plt.title("Countries cumulative GDP 1800-2020")
plt.tight_layout()
plt.show()
```
Ok, better, there are large differences between countries, but we cannot distinguish the individual countries. Lets group countries by region. We will need to download and read in the regions file, then merge the regions dataframe onto the our GDP and life expencancy dataframes.

Read the regions csv into python
```python
regions = pd.read_csv("~/regions.csv")
```
We will merge regions onto gdp_index. The pandas function <a href='https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html' target='_blank'>merge</a> is similar to the SQL merge function this function. It requires a common column name in the two dataframes. 
```python
regions.columns # we need to change the index Country to country in the regions dataframe. Then we can merge it with the index 'country' in gdp_index
regions.columns = ['country','regions']
gdp_index = pd.merge(gdp_index, regions, on=['country'])
```
Let's plot gdp_index grouping by region.

```python
plt.bar(gdp_index['regions'], gdp_index['cumulative'])
plt.xticks(rotation=45)
plt.xlabel('Region')
plt.ylabel('Indexed cumulative GDP')
plt.title("Regions cumulative GDP 1800-2020")
plt.tight_layout()
plt.show()
```
That looks better, we can see that 
How about we map the data. Read the shapefile in, check it's column names then merge the cumulative gdp score onto it.

```python

world = gpd.read_file("~/world/TM_WORLD_BORDERS-0.3.shp")

world.columns  # get the column names. we will need to change NAME to country so that we can merge columns from gpd_index onto it.
world['NAME'] # lets check that NAME is country names. yep it is
world.rename(columns={"NAME":"country"}, inplace=True)
world = world.merge(gdp_index, on='country')
# we will also plot the regions. to do this we will need to disolve the regions so that we have an outline for each region
world_regions = world.dissolve(by='REGION')

world.plot(column='cumulative',cmap='inferno',legend=True,legend_kwds={'label': "Countries cumulative GDP 1800-2020",'orientation': "horizontal"}) # https://matplotlib.org/stable/tutorials/colors/colormaps.html to find cmaps (i.e. colour maps)
plt.show()
```


```python

lowestLE = countriesDat[0].loc[gdp_index['cumulative'].idxmin()] # idxmin gets the index position of the minimum value, i.e. a value that can be used to subset the dataset based on the lowest cumulative gdp
lowestGDP = countriesDat[1].loc[gdp_index['cumulative'].idxmin()]

highestLE = countriesDat[0].loc[gdp_index['cumulative'].idxmax()]
highestGDP = countriesDat[1].loc[gdp_index['cumulative'].idxmax()]

dat = pd.DataFrame([lowestLE,lowestGDP,highestLE,highestGDP]).T
dat.columns = ['lowestLE','lowestGDP','highestLE','highestGDP']
```
Plot them against each other using the plotnine package
```python

(ggplot(dat)  # What data to use
+ aes(x="lowestLE", y="lowestGDP")  # What variable to use
+ geom_point()  # Geometric object to use for drawing
+ labs(title='Life expectency vs GDP', x='life expectancy', y='GDP') # customizing labels
)
```