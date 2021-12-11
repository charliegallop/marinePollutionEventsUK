# %%

import os
import numpy as np
import pandas as pd

n = 10000
years = ['2009']

rawData = pd.read_csv(f"../../data/rawData/{years[0]}_waterQuality.csv")
# %%

# drop columns that are not needed
df1 = rawData.drop(['sample.samplingPoint', 'codedResultInterpretation.interpretation', 'sample.isComplianceSample'], axis = 1)

# remove the unecessary strings from the id column
df1['@id'] = rawData['@id'].astype(str).str[-15:]

# %%

# Selecting only the samples from sea water

dfSea = df1[df1['sample.sampledMaterialType.label'] == 'SEA WATER']

# %%
