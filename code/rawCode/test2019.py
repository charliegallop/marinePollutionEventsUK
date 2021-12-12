# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 


# %%

n = 10000
years = ['2019']
years.reverse()
years = years

# %%

rawData = pd.read_csv(f"/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/rawData/2019_waterQuality.csv")

# %%

# Selecting only the samples from sea water
dfSea = rawData[rawData['sample.sampledMaterialType.label'] == 'SEA WATER']

# Remove time from dataTime column
dfSea['sample.sampleDateTime'] = dfSea['sample.sampleDateTime'].astype(str).str[:10]

## #seperate dateTime column into day, month, year columns
# dfSea[['year', 'month', 'day']] = dfSea['sample.sampleDateTime'].str.split('-', expand = True)

# drop columns that are not needed
dfSea = dfSea.drop(['sample.samplingPoint', 'codedResultInterpretation.interpretation', 'sample.isComplianceSample', 'sample.sampledMaterialType.label', 'sample.purpose.label', 'determinand.unit.label', 'determinand.definition', 'resultQualifier.notation'], axis = 1)

# remove the unecessary strings from the id column
dfSea['@id'] = dfSea['@id'].astype(str).str[-15:]


# %%
dfSeaP = pd.pivot_table(dfSea, values = 'result', index = ['@id'], columns = 'determinand.label')
# %%

def tidyData(fileYear):


    rawData = pd.read_csv(f"/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/rawData/{fileYear}_waterQuality.csv")

    # Selecting only the samples from sea water
    dfSea = rawData[rawData['sample.sampledMaterialType.label'] == 'SEA WATER']

    # Remove time from dataTime column
    dfSea['sample.sampleDateTime'] = dfSea['sample.sampleDateTime'].astype(str).str[:10]

    ## #seperate dateTime column into day, month, year columns
    # dfSea[['year', 'month', 'day']] = dfSea['sample.sampleDateTime'].str.split('-', expand = True)

    # drop columns that are not needed
    dfSea = dfSea.drop(['sample.samplingPoint', 'codedResultInterpretation.interpretation', 'sample.isComplianceSample'], axis = 1)

    # remove the unecessary strings from the id column
    dfSea['@id'] = dfSea['@id'].astype(str).str[-15:]

    # dfSea Pivotted
    dfSeaP = pd.pivot_table(dfSea, values = 'result', index = ['@id'], columns = 'determinand.label')
    dfSeaP = dfSeaP.dropna(axis=1, how='all')
    dfSeaPMerged = dfSeaP.merge(dfSea[['@id', 'sample.samplingPoint.notation', 'sample.samplingPoint.label',
        'sample.samplingPoint.easting', 'sample.samplingPoint.northing', 'sample.sampleDateTime']], how = 'left', on = '@id')
    dfSeaPMerged.head()

    # Group together so that each recording for each data and location is grouped together
    dfSeaPMerged = dfSeaPMerged.groupby(['sample.sampleDateTime', 'sample.samplingPoint.label', 'sample.samplingPoint.easting', 'sample.samplingPoint.northing']).sum().reset_index()


    return dfSeaPMerged

  #  dfSeaPMerged.to_csv(f'/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/{fileYear}_waterQuality_tidy.csv')


# for count, year in enumerate(years):
#     if count == 0:
#         print(f"working on {year}")
#         df = tidyData(year)
#     else:
#         print(f"working on {year}")
#         df2 = tidyData(year)
#         df = pd.concat([df, df2], ignore_index = True)

# df.to_csv(f'/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/all_waterQual.csv')

   
df2019 = tidyData('2019')
df2019.to_csv(f'/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/df2019.csv')
