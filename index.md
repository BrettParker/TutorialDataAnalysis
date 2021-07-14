---
layout: default
---
## Data for this class

<a href="./files/gdp.csv" target="_blank">GDP</a> <br>
<a href="./files/life_expectancy_years.csv" target="_blank">life expectancy</a> <br>
Gap minder data is also avaliable from: https://www.gapminder.org/data/ <br>

## Use a loop to read in the csv files

```python
import glob
import pandas as pd

countriesDat = list() # read csv's into a list
info = [] # so we know which csv's are in the list

for i in glob.glob("/Users/s5001793/Documents/SWC/python/extra_practice/assets/files/*csv"):
    countriesDat.append(pd.read_csv(i))
    info.append(i)
```
The first dataset is life expentancy i.e. countriesDat[0] and the second is GDP i.e. countriesDat[1]

## Lets explore the layout of the data
```python
countriesDat
```
The year is projected to 2100, lets index it to 2020. Remember: iloc is for indexing by the number of the [column,row], while loc uses the labels. Lets also name the rows using country name, which is currently a column. Then we can remove the country column.

```python
for i in range(0,len(countriesDat)):
    cols = countriesDat[i].loc[:,:"country"] # get the country name, which is in the first row
    countriesDat[i].index = cols # add the country name to the index, i.e. the row name
    countriesDat[i] = countriesDat[i].loc[:,"1800":"2020"] # subset the datasets between the years 1800 and 2020
```

Lets have a look at the summary statistics for life expectancy across all countries.

```python
countriesDat[0].describe()
```
If you look at the min, max and mean, looks like they are all increasing, that a good sign. But there looks like there is a big difference between the min and the max.

## Order countries from richest to poorest
Create a function that averages the 

```python
