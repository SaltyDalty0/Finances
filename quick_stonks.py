#!/usr/bin/python -tt
#credit to: [The Infinite Fund, youtube video, https://github.com/kevinkurek/Random_Projects/blob/master/Time_Series_For_Stocks.ipynb]
#check link for statistical significance measure to add more 

import pandas as pd
import numpy as np
import datetime
from pandas_datareader.data import DataReader
import yfinance as yf

#adjust to run through entire portfolio, add to buy sell hold ml project with weighted value depending on statistical significance.

#general datareader
def pandas_read_data(ticker, data_source, start_date, end_date):
    
    df = DataReader(ticker, data_source, start_date, end_date) #interval ='1m'
    print(df.head())
	
    return df
#for higher frequency data and analysis
def yahoo_read_data(ticker = 'AAPL', range = '5d' , freq = '1m'): #all inputs are string
	 
	df = yf.download(ticker,period = range, interval=freq)
	print(df.head())
	
	return df

end_date = datetime.datetime.today().strftime('%Y-%m-%d')

#set ticker symbol here
ticker = 'FCEL'  #'BTC-USD'

#VALE = yahoo_read_data(ticker,'5d','1m')

VALE= pandas_read_data(ticker, 'yahoo', '2020-06-01', end_date)

def autocorr_daily(df):
    """
    Input: DataFrame of ticker from above
    Output: If the ticker is mean reverting or trending daily
    
    daily since df is sampled by days change fequency here or add more checks for hourly and such
    """
    #for bitcoin
    #def custom_resampler(array_like): return np.sum(array_like)/len(array_like)
    #df_resamp = df.resample('1440T').apply(custom_resampler) #resample for desired interval of prediction
    #print(df_resamp.head())

    returns = df.pct_change()   #change to df_resamp
    autocorrelation = returns['Adj Close'].autocorr()

    if autocorrelation < 0:
        print('Ticker {} is daily mean reverting with autocorrelation: {}'.format(ticker, autocorrelation))
    else:
        print('Ticker {} is daily momentum bound or trending with autocorrelation: {}'.format(ticker, autocorrelation))
    
    return

def autocorr_weekly(df):
    """Input: DataFrame of ticker from above
        Output: If the ticker is mean reverting or trending weekly"""
    
    ticker_weekly = df.resample(rule='W').last()
    returns = ticker_weekly.pct_change()
    autocorrelation = returns['Adj Close'].autocorr()
    
    if autocorrelation < 0:
        print('Ticker {} is weekly mean reverting with autocorrelation: {}'.format(ticker, autocorrelation))
    else:
        print('Ticker {} is weekly momentum bound or trending with autocorrelation: {}'.format(ticker, autocorrelation))
    
    return


autocorr_daily(VALE)
autocorr_weekly(VALE)