
# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

n = 10000
years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
years.reverse()
determinandsOfInterest = ['E.coli C-MF', 'Bac All', 'Bac Ruminant', 'Horse Bact', 'Human Mito', 'IE Conf', 'Salinity', 'SewageDebris', 'Temp Water', 'pH', 'BW: Plastics', 'BWP - A.B.', 'BWP - A.F.', 'BWP - Ma', 'BWP - O.L.']
tidyDataDir = '/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData' 
# %%

# The process for tidying a single csv
def tidyData(fileYear, DOI):
    
    # The process for tidying a single csv
    
    
    
    rawData = pd.read_csv(f"/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/rawData/{fileYear}_waterQuality.csv")

    # Selecting only the samples from sea water
    dfSea = rawData.loc[(rawData['sample.sampledMaterialType.label'] == 'SEA WATER')] # | (rawData['sample.sampledMaterialType.label'] == 'ESTUARINE WATER')

    # Remove time from dataTime column
    dfSea['sample.sampleDateTime'] = dfSea['sample.sampleDateTime'].astype(str).str[:10]

    ## #seperate dateTime column into day, month, year columns
    # dfSea[['year', 'month', 'day']] = dfSea['sample.sampleDateTime'].str.split('-', expand = True)

    # drop columns that are not needed
    dfSea = dfSea.drop(['sample.samplingPoint', 'codedResultInterpretation.interpretation', 'sample.isComplianceSample'], axis = 1)

    # remove the unecessary strings from the id column
    dfSea['@id'] = dfSea['@id'].astype(str).str[-15:]


    # Select only the determinands of interest before pivotting
    dfSea = dfSea[dfSea['determinand.label'].isin(DOI)]

   
    # dfSea Pivotted
    dfSeaP = pd.pivot_table(dfSea, values = 'result', index = ['@id'], columns = 'determinand.label', fill_value=None)
    
    # dfSeaP = dfSeaP.dropna(axis=1, how='all')
    dfSeaPMerged = dfSeaP.merge(dfSea[['@id', 'sample.samplingPoint.notation', 'sample.samplingPoint.label',
        'sample.samplingPoint.easting', 'sample.samplingPoint.northing', 'sample.sampleDateTime']], how = 'left', on = '@id')
    
    dfSeaPMerged = dfSeaPMerged.rename(columns = {'sample.sampleDateTime':'Date', 'sample.samplingPoint.label':'location', 'sample.samplingPoint.easting':'easting', 'sample.samplingPoint.northing':'northing'})
  
    dfSeaPMerged = dfSeaPMerged.groupby(by=['sample.samplingPoint.notation', 'location', 'easting', 'northing', 'Date']).mean().reset_index()
    return dfSeaPMerged
   

    ## Group together so that each recording for each data and location is grouped together
    #dfSeaPMerged = dfSeaPMerged.groupby(['sample.sampleDateTime', 'sample.samplingPoint.label', 'sample.samplingPoint.easting', 'sample.samplingPoint.northing'], dropna = False).sum().reset_index()
   
    



def makeMergedCSV(years, saveTo, nameOutput):
    
    # This takes in each file in the data folder for the defined years and
    # does the respective cleaning and pivoting of the data to get it into useable
    # format. It then appends all the years together and saves the output as a
    # csv

  #  dfSeaPMerged.to_csv(f'/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/{fileYear}_waterQuality_tidy.csv')


    for count, year in enumerate(years):
        if count == 0:
            print(f"working on {year}")
            df = tidyData(year, determinandsOfInterest)
            print(f"succesfully finished {year}")
        else:
            print(f"working on {year}")
            df2 = tidyData(year, determinandsOfInterest)
            df = pd.concat([df, df2], ignore_index = True)
            print(f"succesfully finished {year}")
            
    print("finished merge succesfully")
    df.to_csv(f'{saveTo}/{nameOutput}')
    print(f"saved as csv to {saveTo}/{nameOutput}")
    

# %%
makeMergedCSV(years, tidyDataDir, 'all_waterQual.csv')



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