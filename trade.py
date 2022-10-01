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

symbol = 'APPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
data = requests.get(api_url)
print(data.status_code)
