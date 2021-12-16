# %%
import netCDF4 as nc
import numpy as np
import numpy.ma as ma
import pandas as pd
import seaborn as sns


#%%

def Rainfall3DArray(fileName, fileLocation):
    import netCDF4 as nc
    import numpy as np
    import numpy.ma as ma
    import pandas as pd

    locationOfFile = fileLocation
    fileName = fileName
    
    # Load the netCDF dataset in
    
    ds = nc.Dataset(f'{locationOfFile}{fileName}')
    
    # Create a list containing the 1251x701 2d grid matrix of rainfall for each
    # day. Where the x value (1251) is the y northing and the y value
    # (701) is the x easting of the sample location.
    
    days = ds['rainfall_amount'].shape[0]
    rainDaysList = []
    
    for day in range(days):
        if day == 0:
            rainDaysList =  [pd.DataFrame(ds['rainfall_amount'][day])]
        else:
            rainDaysList.append(pd.DataFrame(ds['rainfall_amount'][day]))
            
    return rainDaysList


#%%

rainfall2019 = Rainfall3DArray('2019_daily_rainfall.nc', '/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/rawData/')


# %%

# Print the variables in the dataset
print(ds.variables.keys())

# %%
print(ds.variables['rainfall_amount']) # look at variable description



# %%

# Extract the masked array for rainfall on a given day. Returns a 1251x701 
# 2D matrix grid where the x value (1251) is the y northing and the y value
# (701) is the x easting of the sample location. Can also load all 365 layers
# with rainfall = ds['rainfall_amount'][:]

# rainfall0 = ds['rainfall_amount'][day]
# rainfall1 = ds['rainfall_amount'][day+1]



# %%

# This selects all the x and y coordinates and saves them in arrays for ease
# of indexing.For rainfall value at any location it is the rainfall indexes 
# flipped with the maxY-y all /1000 i.e. for the rainfall at gr x: 159,000, 
# y: 35,000 (which are eastings and northings from the waterQual data) 
# it would be rainfall[maxY-y/1000, x/1000]

x = ds['x'][:].data[:]
y = ds['y'][:].data[:]

# %%
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import style
import matplotlib.animation as animation
maxY = y.max()
fig, ax = plt.subplots()

cmap = matplotlib.cm.get_cmap("jet").copy()
cmap.set_bad('white', 1.)
# plot
ax.imshow(rainDaysList[17], interpolation='nearest', cmap='viridis_r')

plt.show()

# %%

print(rainDaysList[0][505][248])

# %%

# Function for estimating the rainfall for locations that are out of bounds
# in the rainfall data. It takes an average of the non-nan values up to k 
# neighbours
def estRain(x, y, data, day, neighbors):
    df = data[day]
    x, y = x, y
    numn = neighbors
    # nn = np.empty((numn+7, numn+7))
    nn = np.empty(0)
    for i in range(-numn, numn + 1):
        templist = np.empty(0)
        for j in range(-numn, numn + 1):
            valNeighbour = df.iloc[x + i, y + j]
            templist = np.append(templist, [valNeighbour], axis = 0)
        nn = np.append(nn, templist, axis = 0)
    
    nearest_neighbours = nn.reshape(numn*2+1, numn*2+1)
    return np.nanmean(nearest_neighbours)

    
nn = estRain(505, 248, rainDaysList, 0, 10)