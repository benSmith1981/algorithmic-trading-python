import numpy as np #The Numpy numerical computing library
import pandas as pd #The Pandas data science library
import requests #The requests library for HTTP requests in Python
import xlsxwriter #The XlsxWriter libarary for 
import math #The Python math module
from scipy import stats #The SciPy stats module

stocks = pd.read_csv('sp_500_stocks.csv')
from secrets import IEX_CLOUD_API_TOKEN


# Function sourced from 
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]   
        
symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
#     print(symbol_strings[i])

my_columns = ['Ticker', 'Price', 'One-Year Price Return', 'Number of Shares to Buy']

final_dataframe = pd.DataFrame(columns = my_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=price,stats&token={IEX_CLOUD_API_TOKEN}'
    print(batch_api_call_url)
    data = requests.get(batch_api_call_url).json()
    #print(data)
    for symbol in symbol_string.split(','): #for every symbol in comma separated string, loop over the data to get the data from each to add to series
        if symbol in data:
            final_dataframe = final_dataframe.append(
                                            pd.Series([symbol, 
                                                    data[symbol]['price'],
                                                    data[symbol]['stats']['year1ChangePercent'],
                                                    'N/A'
                                                    ], 
                                                    index = my_columns), 
                                            ignore_index = True)
        
    
final_dataframe.sort_values('One-Year Price Return', ascending = False, inplace = True) #inplace = true modifies the original data frame
final_dataframe = final_dataframe[:51]
final_dataframe.reset_index(drop = True, inplace = True)
print(final_dataframe)