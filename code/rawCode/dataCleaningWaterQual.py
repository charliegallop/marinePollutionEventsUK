# %%

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

# %%
n = 10000
years = ['2009']

rawData = pd.read_csv(f"../../data/rawData/{years[0]}_waterQuality.csv")
# %%

# Selecting only the samples from sea water
dfSea = rawData[rawData['sample.sampledMaterialType.label'] == 'SEA WATER']
# %%
# Remove time from dataTime column
dfSea['sample.sampleDateTime'] = rawData['sample.sampleDateTime'].astype(str).str[:10]

# %%
#seperate dateTime column into day, month, year columns
dfSea[['year', 'month', 'day']] = dfSea['sample.sampleDateTime'].str.split('-', expand = True)

# %%
# drop columns that are not needed
dfSea = rawData.drop(['sample.samplingPoint', 'codedResultInterpretation.interpretation', 'sample.isComplianceSample', 'sample.sampleDateTime'], axis = 1)

# %%
# remove the unecessary strings from the id column
dfSea['@id'] = rawData['@id'].astype(str).str[-15:]


# %%
dfEcoli = dfSea[dfSea['determinand.label'] == "E.coli C-MF"]
dfEcoli = dfEcoli[dfEcoli['result'] > 500]
plt.hist(dfEcoli['result'], bins = [100, 200, 300, 400, 500, 600, 700])


# %%
