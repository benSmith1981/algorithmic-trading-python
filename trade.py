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
print(data)
