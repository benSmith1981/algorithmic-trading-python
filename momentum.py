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

# for symbol_string in symbol_strings:
#     batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=price,stats&token={IEX_CLOUD_API_TOKEN}'
#     data = requests.get(batch_api_call_url).json()
#     #print(data)
#     for symbol in symbol_string.split(','): #for every symbol in comma separated string, loop over the data to get the data from each to add to series
#         if symbol in data:
#             final_dataframe = final_dataframe.append(
#                                             pd.Series([symbol, 
#                                                     data[symbol]['price'],
#                                                     data[symbol]['stats']['year1ChangePercent'],
#                                                     'N/A'
#                                                     ], 
#                                                     index = my_columns), 
#                                             ignore_index = True)
        
    
# final_dataframe.sort_values('One-Year Price Return', ascending = False, inplace = True) #inplace = true modifies the original data frame
# final_dataframe = final_dataframe[:51] #drops stocks outside top 50
# final_dataframe.reset_index(drop = True, inplace = True) #inplace = true modifies the original data frame
# print(final_dataframe) 


def portfolio_input():
    global portfolio_size
    portfolio_size = input("Enter the value of your portfolio:")

    try:
        val = float(portfolio_size)
    except ValueError:
        print("That's not a number! \n Try again:")
        portfolio_size = input("Enter the value of your portfolio:")

# portfolio_input()
# print(portfolio_size)

# position_size = float(portfolio_size) / len(final_dataframe.index)
# for i in range(0, len(final_dataframe['Ticker'])):
#     final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size / final_dataframe['Price'][i])
# final_dataframe

hqm_columns = [
    'Ticker',
    'Price',
    'Number of Shares to Buy',
    'One-Year Price Return',
    'One-Year Return Percentile',
    'Six-Month Price Return',
    'Six-Month Return Percentile',
    'Three-Month Price Return',
    'Three-Month Return Percentile',
    'One-Month Price Return',
    'One-Month Return Percentile'
]

hqm_dataframe = pd.DataFrame(columns = hqm_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=price,stats&token={IEX_CLOUD_API_TOKEN}'

    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','): #for every symbol in comma separated string, loop over the data to get the data from each to add to series
        if symbol in data:
            hqm_dataframe = hqm_dataframe.append(
                                pd.Series([
                                            symbol,
                                            data[symbol]['price'],
                                            'Number of Shares to Buy',
                                            data[symbol]['stats']['year1ChangePercent'],
                                            'N/A',#One-Year Return Percentile',
                                            data[symbol]['stats']['month6ChangePercent'],
                                            'N/A',#'Six-Month Return Percentile',
                                            data[symbol]['stats']['month3ChangePercent'],
                                            'N/A',#'Three-Month Return Percentile',
                                            data[symbol]['stats']['month1ChangePercent'],
                                            'N/A',#'One-Month Return Percentile'
                                        ], 
                                        index = hqm_columns), 
                                ignore_index = True)

time_periods = [
                'One-Year',
                'Six-Month',
                'Three-Month',
                'One-Month'
                ]

for row in hqm_dataframe.index: #look through rows of hqm dataframe
    for time_period in time_periods: #llop trhough time periods
        #panda loc method changes the value of each time period column
        #stats.percentileofscore takes two arguments, 1st entire column, 2nd entry from that column
        print(hqm_dataframe.loc[row, f'{time_period} Price Return']/100)

        hqm_dataframe.loc[row, f'{time_period} Return Percentile'] = stats.percentileofscore(hqm_dataframe[f'{time_period} Price Return'], hqm_dataframe.loc[row, f'{time_period} Price Return'])/100
#print(hqm_dataframe)
