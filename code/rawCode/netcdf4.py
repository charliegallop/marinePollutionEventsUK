# %%

import netCDF4 as nc
import numpy as np

fn = "CEH_GEAR_monthly_GB_2019.nc"

ds = nc.Dataset(fn)
rainfall = ds['rainfall_amount'][:]
y = ds['y'][:]
x = ds['x'][:]
time = ds['time'][:]
# %%
rainfall[1, 10, 10]
# %%
for i in range(12):
    print(rainfall[i, 501, 351])
    print(y[501])
    print(x[351])

# %%

print(ds.variables.keys()) # get all variable names

# %%
sst = ds.variables['rainfall_amount'] # sst variable
time = ds.variables['time']
print(time)

# %%
