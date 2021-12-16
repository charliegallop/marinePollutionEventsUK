# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
# %%
rainfallDf = pd.read_pickle('/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/pickleData/rainfall2019.pkl')
rainfallDf = rainfallDf[0]
importedDf = pd.read_csv('/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/all_waterQual.csv')
# %%
df = importedDf
df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')

df.set_index("Date", inplace = True)

# Create a column that is the day of the year each sampling point was taken.
# This will be used to join the rainfall data to

df['dayOfYear'] = df.index.day_of_year
df.drop('Unnamed: 0', axis = 1, inplace = True)

# %%
# Columns in data frame:
# ['sample.samplingPoint.notation', 'location', 'easting', 'northing',
#        'BW: Plastics', 'BWP - A.B.', 'BWP - A.F.', 'BWP - Ma', 'BWP - O.L.',
#        'Bac All', 'Bac Ruminant', 'E.coli C-MF', 'Horse Bact', 'Human Mito',
#        'IE Conf', 'Salinity', 'SewageDebris', 'Temp Water', 'pH', 'dayOfYear']

#%%

df['eastingNorm'] = df.apply(lambda x: math.floor(x.easting/1000), axis = 1)
df['northingNorm'] = df.apply(lambda x: math.floor(x.easting/1000), axis = 1)


#%%
x = df[(df['Temp Water'] > 0) & (df['E.coli C-MF'] > 0)][['Temp Water', 'E.coli C-MF']]
plt.scatter(x = x['Temp Water'], y = x['E.coli C-MF'], alpha = 0.5)

# %%
df.loc[(df[y] > 0) & (df['location'] == 'TYNEMOUTH CULLERCOATS (04900)') & (df[x] > 0) & (df[x] < 20)].plot(kind = "scatter", x = x, y =y, alpha = 0.5)


# %%

def getRainfall(df):
    df = df
    df['rainfall'] = rainfallDf[rainfallDf[(df['eastingNorm'])][(df['northingNorm'])]]

# %%

# df["xRainfallCoords"] = round((1250000 - df['northing'])/1000)
# df["yRainfallCoords"] = round(df['easting']/1000)

# %%

# x = df['xRainfallCoords'].loc[(df['location'] == 'CULLERCOATS BW INVESTIG 2 : BEDROCK POOL') & (df['Date'] == '2019-01-03 00:00:00')]
# y = df['yRainfallCoords'].loc[(df['location'] == 'CULLERCOATS BW INVESTIG 2 : BEDROCK POOL') & (df['Date'] == '2019-01-03 00:00:00')]
# x = int(x.values[0])
# y = int(y.values[0])


# %%

rainDf300 = pd.read_csv("/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/300rainfallMatrix.csv")

# Function for estimating the rainfall for locations that are out of bounds
# in the rainfall data. It takes an average of the non-nan values up to k 
# neighbours
def estRain(x, y, data, neighbors):
    df = data
    x, y = x, y
    numn = neighbors
    # nn = np.empty((numn+7, numn+7))
    nn = []
    for i in range(-numn, numn + 1):
        templist = []
        for j in range(-numn, numn + 1):
            valNeighbour = df.iloc[x + i, y + j]
            templist.append(valNeighbour)
        nn.append(templist)
    
    nearest_neighbours = np.array(nn)
    return np.nanmean(nearest_neighbours)

    
print(estRain(x, y, rainDf300, 5))

# %%

# # %%
# # convert the date time on the water quality df to day of the year so it can be matched witht the rainfall

# from datetime import datetime
# day_of_year = df['Date'][600].strftime('%j')


# # %%


# rawdf = pd.read_csv("/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/rawData/2019_waterQuality.csv")
# #alldf = pd.read_csv("/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/all_waterQual.csv")
# seaOnlyDf = pd.read_csv("/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/all_waterQual.csv")

# # %%

# dfCols = seaOnlyDf.columns
# dfCols = dfCols.tolist()
# dfCols = pd.DataFrame(dfCols, columns = ["determinand.label"])


# detDescDf = pd.merge(dfCols, rawdf[['determinand.label', 'determinand.definition']], on = 'determinand.label', how = "inner", ).drop_duplicates(subset=['determinand.label'], keep='first')


# detDescDf.to_csv("/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/determinandDescriptions.csv")
# print("File created succesfully")