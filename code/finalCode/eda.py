# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %%

d_parser = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
df = pd.read_csv('/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/all_waterQual.csv', parse_dates=['sample.sampleDateTime'], date_parser = d_parser)
# %%

df = df.rename(columns = {'sample.sampleDateTime':'Date', 'sample.samplingPoint.label':'location', 'sample.samplingPoint.easting':'easting', 'sample.samplingPoint.northing':'northing'})

df['Date'].nunique()
df.columns
df['location']
# %%
y = 'IE Conf'
x = 'Temp Water'
df.loc[(df[y] > 0) & (df[x] > 0)].plot(kind = 'scatter', x = x, y = y, alpha = 0.5)

# %%
df.loc[(df[y] >= 0) & (df['location'] == 'TYNEMOUTH CULLERCOATS (04900)') & (df[x] > 0) & (df[x] < 20)].plot(kind = "scatter", x = x, y =y, alpha = 0.5)


# %%


df["xRainfallCoords"] = round((1250000 - df['northing'])/1000)
df["yRainfallCoords"] = round(df['easting']/1000)

# %%

x = df['xRainfallCoords'].loc[(df['location'] == 'CULLERCOATS BW INVESTIG 2 : BEDROCK POOL') & (df['Date'] == '2019-01-03 00:00:00')]
y = df['yRainfallCoords'].loc[(df['location'] == 'CULLERCOATS BW INVESTIG 2 : BEDROCK POOL') & (df['Date'] == '2019-01-03 00:00:00')]



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



estRain(x, y, rainDf, 10)



# %%





# %%
# convert the date time on the water quality df to day of the year so it can be matched witht the rainfall

from datetime import datetime
day_of_year = df['Date'][600].strftime('%j')



# %%


rawdf = pd.read_csv("/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/rawData/2019_waterQuality.csv")
#alldf = pd.read_csv("/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/all_waterQual.csv")
seaOnlyDf = pd.read_csv("/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/all_waterQual.csv")

# %%

dfCols = seaOnlyDf.columns
dfCols = dfCols.tolist()
dfCols = pd.DataFrame(dfCols, columns = ["determinand.label"])


detDescDf = pd.merge(dfCols, rawdf[['determinand.label', 'determinand.definition']], on = 'determinand.label', how = "inner", ).drop_duplicates(subset=['determinand.label'], keep='first')


detDescDf.to_csv("/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/tidyData/determinandDescriptions.csv")
print("File created succesfully")