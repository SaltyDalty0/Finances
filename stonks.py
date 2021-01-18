#!/usr/bin/env python3
#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 00:20:40 2020

@author: DaltonGlove
"""

#Simple candlestick plot of a Ticker (Bitcoin for example)
#

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc

import plotly.graph_objects as go
#import mpl_toolkits
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2020,6,1)
end = dt.datetime(2021, 1, 6)
df = web.DataReader(['BTC-USD'], 'yahoo', start, end)
df.dropna(inplace=True)
print(df.head(10), "\n", df.tail(10))


#df.to_csv('bitcoin.csv')
#df = pd.read_csv('bitcoin.csv', parse_dates=True)#, index_col=0)

#df[['Adj Close','Open','High']].plot()

#df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
#df.dropna(inplace=True)
#print(df.head(10))

df.set_index('Date', inplace=True)

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_vol = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)

df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

mpf.plot(df, type='candle', style='charles',
            title='Bitcoin',
            #ylabel='Price ($)',
            #ylabel_lower='Shares \nTraded',
            volume=True,
            mav=(3,6,9),
            savefig='test-mplfiance.png')

#ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
#ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
#ax1.xaxis_date()

#candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
#ax2.fill_between(df_vol.index.map(mdates.date2num), df_vol.values)

#ax1.plot(df.index, df['Adj Close'])
#ax1.plot(df.index, df['100ma'])
#ax2.bar(df.index, df['Volume'])

plt.show()



