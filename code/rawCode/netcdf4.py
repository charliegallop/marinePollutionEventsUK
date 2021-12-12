# %%

import netCDF4 as nc
import numpy as np
import numpy.ma as ma
import pandas as pd
import seaborn as sns

# %%
fn = "/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/rawData/2019_daily_rainfall.nc"

ds = nc.Dataset(fn)

# %%

print(ds.variables.keys()) # get all variable names


# %%
rainfall = ds['rainfall_amount'][:]


# %%
ds.variables['y'] # look at variable description

# %%
x = ds['x'][:]
x = x.data[:]
x

# %%

y = ds['y'][:]
y = y.data[y.data <= 700000]
y


# %%

coord = pd.DataFrame({'x(easting)':x, 'y(northing)':y})
coord = coord.pivot_table(index='x(easting)', columns='y(northing)', fill_value = 0)

#%%
maxY = 1250


import matplotlib.pyplot as plt
import matplotlib
from matplotlib import style
import matplotlib.animation as animation

fig, ax = plt.subplots()

day = 300

rainDf = pd.DataFrame(rainfall.data[day])

rainDf = rainDf.replace(to_replace=-999.0, value = np.nan)

masked_array = np.ma.array(rainDf, mask = np.isnan(rainDf))
cmap = matplotlib.cm.get_cmap("jet").copy()
cmap.set_bad('white', 1.)
# plot
ax.imshow(masked_array, interpolation='nearest', cmap='viridis_r')

plt.show()

# for rainfall value at any location it is the rainfall indexes flipped with the maxY-y all /1000
# i.e. for the rainfall at gr x: 159,000, y: 35,000 it would be rainDf[maxY-y/1000, x/1000]

#%%
rainDf.to_csv(f"/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/{day}rainfallMatrix.csv")

# %%

def estRain(x, y, data, neighbors):
    df = data
    x, y = x, y
    neigh = neighbors
    nn = np.empty((0,0), int)
    for i in range(neigh):
        for j in range(neigh):
            nn = np.append(nn, df.iloc[x - j, y+i])
            nn = np.append(nn, df.iloc[x + j, y+i])
            
    print(np.nanmean(nn))
    
estRain(1200, 231, rainDf, 10)

