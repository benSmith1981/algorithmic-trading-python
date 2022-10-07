import numpy as np #The Numpy numerical computing library
import pandas as pd #The Pandas data science library
import requests #The requests library for HTTP requests in Python
import xlsxwriter #The XlsxWriter libarary for 
import math #The Python math module
from scipy import stats #The SciPy stats module
from scipy.stats import percentileofscore as score #The SciPy stats module
from statistics import mean
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
    'One-Month Return Percentile',
    'HQM Score'
]

hqm_dataframe = pd.DataFrame(columns = hqm_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=price,stats&token={IEX_CLOUD_API_TOKEN}'

    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','): #for every symbol in comma separated string, loop over the data to get the data from each to add to series
        if symbol in data:
            if data[symbol]['stats']['year1ChangePercent'] != None:
                hqm_dataframe = hqm_dataframe.append(
                                    pd.Series([
                                                symbol, 
                                                data[symbol]['price'],
                                                'N/A',
                                                data[symbol]['stats']['year1ChangePercent'],
                                                'N/A',#One-Year Return Percentile',
                                                data[symbol]['stats']['month6ChangePercent'],
                                                'N/A',#'Six-Month Return Percentile',
                                                data[symbol]['stats']['month3ChangePercent'],
                                                'N/A',#'Three-Month Return Percentile',
                                                data[symbol]['stats']['month1ChangePercent'],
                                                'N/A',#'One-Month Return Percentile'
                                                'N/A'
                                            ], 
                                            index = hqm_columns), 
                                    ignore_index = True)

time_periods = [
                'One-Year',
                'Six-Month',
                'Three-Month',
                'One-Month'
                ]

# print(hqm_dataframe[f'{time_period} Price Return'])
# #print(hqm_dataframe.loc[row, f'{time_period} Price Return'])
# print(f'{time_period} Return Percentile')
print(stats.percentileofscore([1,2,3,4],3))
print(f'{time_periods[3]} Return Percentile')
#hqm_dataframe.loc[row, f'{time_period} Return Percentile'] = stats.percentileofscore(hqm_dataframe[f'{time_period} Price Return'])

for row in hqm_dataframe.index: #look through rows of hqm dataframe
    for time_period in time_periods: #llop trhough time periods
        #panda loc method changes the value of each time period column
        #stats.percentileofscore takes two arguments, 1st entire column, 2nd entry from that column
        change_col = f'{time_period} Price Return'
        percentile_col = f'{time_period} Return Percentile'
        if hqm_dataframe.loc[row, change_col] != None:
            #print( hqm_dataframe.loc[row, change_col])
            hqm_dataframe.loc[row, percentile_col] = score(hqm_dataframe[change_col], hqm_dataframe.loc[row, change_col]/100)

for row in hqm_dataframe.index:
    momentum_percentiles = []
    for time_period in time_periods:
        momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
    hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)


hqm_dataframe.sort_values(by = 'HQM Score', ascending = False)
hqm_dataframe = hqm_dataframe[:51]
hqm_dataframe.reset_index(drop = True, inplace = True)


portfolio_input()
print(final_dataframe.index)

position_size = float(portfolio_size) / len(hqm_dataframe.index)

for i in hqm_dataframe.index:
    #if final_dataframe['Price'][i] != None:
    hqm_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size / hqm_dataframe.loc[i,'Price'])
print(hqm_dataframe)


#Output to excel

writer = pd.ExcelWriter('Recommended_equalstrat_trades.xlsx', engine='xlsxwriter')
hqm_dataframe.to_excel(writer, 'Recommended Trades', index=False)

background_color = '#0a0a23'
font_color = '#ffffff'

string_format = writer.book.add_format(
    {
        'font_color': font_color, 
        'bg_color': background_color, 
        'border': 1
    }
)

dollar_format = writer.book.add_format(
    {
        'num_format':'$0.00',
        'font_color': font_color, 
        'bg_color': background_color, 
        'border': 1
    }
)

integer_format = writer.book.add_format(
    {
        'num_format':'0',
        'font_color': font_color, 
        'bg_color': background_color, 
        'border': 1
    }
)

writer.sheets['Recommended Trades'].set_column('A:A', #This tells the method to apply the format to column B
                     18, #This tells the method to apply a column width of 18 pixels
                     string_format #This applies the format 'string_template' to the column
                    )

#use loop below through dictionary 
# writer.sheets['Recommended Trades'].set_column('B:B', 18, string_format)          
# writer.sheets['Recommended Trades'].set_column('C:C', 18, string_format)          
# writer.sheets['Recommended Trades'].set_column('D:D', 18, string_format)          
# writer.sheets['Recommended Trades'].set_column('B:B', 18, string_format)   
# writer.sheets['Recommended Trades'].write('A1', 'Ticker', string_format)
# writer.sheets['Recommended Trades'].write('B1', 'Stock Price', dollar_format)
# writer.sheets['Recommended Trades'].write('C1', 'Market Capitalisation', dollar_format)
# writer.sheets['Recommended Trades'].write('D1', 'Number of shares to buy', integer_format)


column_formats = {
    'A' : ['Ticker', string_format],
    'B' : ['Stock Price', dollar_format],
    'C' : ['Market Capitalisation', dollar_format],

    'D' : ['One-Year Price Return', integer_format],
    'E' : ['One-Year Return Percentile', integer_format],
    'F' : ['Six-Month Price Return', integer_format],
    'G' : ['Six-Month Return Percentile', integer_format],
    'H' : ['Three-Month Price Return', integer_format],
    'I' : ['Three-Month Return Percentile', integer_format],
    'I' : ['One-Month Price Return', integer_format],
    'I' : ['One-Month Return Percentile', integer_format]


}
for column in column_formats.keys():
    writer.sheets['Recommended Trades'].set_column(f'{column}:{column}',18,column_formats[column][1])
    writer.sheets['Recommended Trades'].write(f'{column}1',column_formats[column][0],column_formats[column][1])

writer.save()