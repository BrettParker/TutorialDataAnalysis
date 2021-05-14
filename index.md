---
layout: default
---
## Data for this class

<a href="./files/gdp.csv" target="_blank">GDP</a>
<a href="./files/life_expectancy_years.csv" target="_blank">life expectancy</a>
Gap minder data is also avaliable from: https://www.gapminder.org/data/

## Use a loop to read in the csv files

```python
import glob
import pandas as pd

countriesDat = list() # read csv's into a list
info = [] # so we know which csv's are in the list

for filename in glob.glob("/Users/s5001793/Documents/SWC/python/extra_practice/assets/files/*csv"):
    countriesDat.append(pd.read_csv(filename))
    info.append(filename)
```

## Order countries from richest to poorest
