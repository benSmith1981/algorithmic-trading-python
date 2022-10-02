import os
print(os.getcwd())

import sys
# print(sys.path)
import secrets
print(secrets)
import numpy as np
import pandas as pd
import requests
# import xlswriter
# import math

from secrets import IEX_CLOUD_API_TOKEN
stocks = pd.read_csv('sp_500_stocks.csv')

symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={IEX_CLOUD_API_TOKEN}'
#api_url = f'https://algorithmpython.iex.cloud/v1/data/CORE/HISTORICAL_PRICES?last=1&token={IEX_CLOUD_API_TOKEN}'
#api_url = f'https://algorithmpython.iex.cloud/v1/data/CORE/{symbol}/quote?token={IEX_CLOUD_API_TOKEN}'
#api_url = 'https://sandbox.iexapis.com/stable/stock/AAPL/quote?token=Tpk_059b97af715d417d9f49f50b51b1c448'
data = requests.get(api_url).json()

price = data['latestPrice']
market_price = data['marketCap']

my_columns = ['Ticker','Stock Price', 'Market Capitalization', 'Number of shares to buy']
final_data_frame = pd.DataFrame(columns = my_columns)
# final_data_frame.append(
#     pd.Series(
#         [
#             symbol,
#             price,
#             market_price,
#             'N/A'
#         ],
#         index = my_columns,
#     ),
    
#     ignore_index=True
# )

print(final_data_frame)
# for stock in stocks['Ticker'][:5]:
# #for stock in stocks['Ticker']:
#     print(stock)
#     api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={IEX_CLOUD_API_TOKEN}'
#     data = requests.get(api_url).json()

#     final_data_frame = final_data_frame.append(
#         pd.Series
#             (
#                 [
#                     stock,
#                     data['latestPrice'],
#                     data['marketCap'],
#                     'N/A'
#                 ],
#                 index = my_columns),
#             ignore_index=True
#         )


# print(final_data_frame)


def chunks(l, n):
    """Yield n number of striped chunks from l."""
    for i in range(0,len(l), n):
        yield l[i: i+n]

symbol_groups = list(chunks(stocks['Ticker'], 100))
print(len(symbol_groups))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    print(len(symbol_groups[i]))
    symbol_strings.append(','.join(symbol_groups[i]))

#print(symbol_strings) #create a long string of symbols should

for symbol_string in symbol_strings:
    #insert the long string symbol in here for a batch request, like this:
    #https://sandbox.iexapis.com/stable/stock/market/batch?symbols=ABBV,AEE,ALGN,AMP,APH,AZO,BK,BXP,CCL,CI,CNC,CRM,CXO,DIS,DRI,ED,ESS,F,FISV,FTI,GOOG,HBAN,HON,IBM,IP,J,KHC,L,LMT,MA,MET,MOS,MU,NKE,NUE,ORCL,PEP,PM,PVH,RF,RTX,SNA,SWK,TFC,TSCO,UAL,V,VTR,WLTW,XEL,ZTS&types=quote&token=Tpk_059b97af715d417d9f49f50b51b1c448
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    #print(batch_api_call_url)
    print(symbol_string)
    data = requests.get(batch_api_call_url).json()

    for symbol in symbol_string.split(','):
        if symbol != 'DISCA':
            print(data[symbol])
            final_data_frame = final_data_frame.append(
                pd.Series
                    (
                        [
                            symbol,
                            data[symbol]['quote']['latestPrice'],
                            data[symbol]['quote']['marketCap'],
                            'N/A'
                        ],
                        index = my_columns
                    ),
                    ignore_index=True
            )
#print(final_data_frame)