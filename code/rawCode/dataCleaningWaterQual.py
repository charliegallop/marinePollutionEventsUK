
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

n = 10000
years = ['2009', '2010', '2011', '2012', '2013']

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

    dfSeaPMerged.to_csv(f'/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/{fileYear}_waterQuality_tidy.csv')


for year in years:
    tidyData(year)
   
