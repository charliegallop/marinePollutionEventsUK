import requests
import os

# domain = 'https://catalogue.ceh.ac.uk/datastore/eidchub/dbf13dd5-90cd-457a-a986-f2f9dd97e93c/GB/daily/'
# year = '2019'
# fileName = f'CEH_GEAR_daily_GB_{year}.nc'
# downloadURL = f'{domain}{fileName}'

url = 'https://catalogue.ceh.ac.uk/datastore/eidchub/dbf13dd5-90cd-457a-a986-f2f9dd97e93c/GB/daily/CEH_GEAR_daily_GB_1895.nc'

import requests

from clint.textui import progress

r = requests.get(url, stream=True)

with open("CEH_GEAR_daily_GB_1895.nc", "wb") as f:

    total_length = int(r.headers.get('content-length'))

    for ch in progress.bar(r.iter_content(chunk_size = 2391975), expected_size=(total_length/1024) + 1):

        if ch:

            f.write(ch)
            


  
# def DownloadFile(url, fileName='', year=''):
#     os.chdir('/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/rawData')
#     try:
#         with requests.get(url, stream = True) as r:
#             with open(fileName, "wb") as f:
#                 for chunk in r.iter_content(chunk_size=(8192)):
#                     if chunk:
#                         f.write(chunk)
#                         f.flush()
#             os.chdir('/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project')
#             print('completed')
#             return fileName
#     except Exception as e:
#         print(e)
#         return None

 
# DownloadFile(domain, fileName, year)

# # # def GetNCFIle(year):
   
# # #     # Check to see if file is already downloaded
# # #     if 










# import asyncio
# import concurrent.futures
# import requests
# import os

# domain = 'https://catalogue.ceh.ac.uk/datastore/eidchub/dbf13dd5-90cd-457a-a986-f2f9dd97e93c/GB/daily/'
# year = '2019'
# fileName = f'CEH_GEAR_daily_GB_{year}.nc'
# downloadURL = f'{domain}{fileName}'

# async def get_size(url):
#     response = requests.head(url)
#     size = int(response.headers['Content-Length'])
#     return size


# def download_range(url, start, end, output):
#     headers = {'Range': f'bytes={start}-{end}'}
#     response = requests.get(url, headers=headers)

#     with open(output, 'wb') as f:
#         for part in response.iter_content(1024):
#             f.write(part)


# async def download(executor, url, output, chunk_size=1000000):
#     loop = asyncio.get_event_loop()

#     file_size = await get_size(url)
#     chunks = range(0, file_size, chunk_size)

#     tasks = [
#         loop.run_in_executor(
#             executor,
#             download_range,
#             url,
#             start,
#             start + chunk_size - 1,
#             f'{output}.part{i}',
#         )
#         for i, start in enumerate(chunks)
#     ]

#     await asyncio.wait(tasks)

#     with open(output, 'wb') as o:
#         for i in range(len(chunks)):
#             chunk_path = f'{output}.part{i}'

#             with open(chunk_path, 'rb') as s:
#                 o.write(s.read())

#             os.remove(chunk_path)


# if __name__ == '__main__':
#     executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
#     loop = asyncio.get_event_loop()

#     try:
#         loop.run_until_complete(
#             download(executor, downloadURL, fileName)
#         )
#     finally:
#         loop.close()