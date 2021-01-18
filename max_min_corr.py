# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 00:21:40 2020

Project parts 2 & 3: 
    filtering index funds for negatively correlated stocks to hedge
    and filtering for postively correlated stock to pair

this is adjusted from moreStonks.py file just adding to sort and print out max and min correlated stocks in df
    

@author: Dalton Glove with credit to 
"""
import bs4 as bs
import pickle
import requests

import matplotlib.pyplot as plt

import datetime as dt
import os
import pandas as pd
from pandas_datareader import data as pdr
import numpy as np

#import fix_yahoo_finance as yf
import yfinance as yf
yf.pdr_override()



def save_sp500_tickers():
    #headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
    
    #df = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    #df.columns = df.ix[0]
    #df.drop(df.index[0], inplace=True)
    
    
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
                        #headers=headers)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    #table = soup.find('table', {'class':'wikitable sortable'})
    table = soup.find('table', {'id': 'constituents'})
    #print(table)
    tickers=[]
    for row in table.findAll('tr')[1:]:
        #ticker = row.findAll('td')[1].text.replace('.', '-')
        ticker = row.find('td').text.replace('.', '-')
        #ticker = ticker[:-1]
        tickers+=[ticker.strip()]
        #print(ticker)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    print(tickers)
    
    return tickers

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
            
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start = dt.datetime(2005, 1, 1)
    end = dt.datetime(2020, 11, 25)
    
    for ticker in tickers:
      """adjusted webscraping to using fix_yahoo import so retry and regenerate dfs"""
      try:
        if not os.path.exists('stocks_dfs/{}.csv'.format(ticker)):
            df = pdr.get_data_yahoo(ticker,start, end)             #pdr.DataReader(ticker,'yahoo',start,end)  #pdr.get_data_yahoo(ticker, start, end)
            df.reset_index(inplace=True)
            df.set_index('Date', inplace=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
            print('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
      except KeyError: pass


def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    
    main_df = pd.DataFrame()
    print(main_df.head())
    start = dt.datetime(2005, 1, 1)
    end = dt.datetime(2020, 7, 3)
    for count, ticker in enumerate(tickers):
      try:
        #if ticker=='CARR' or ticker=='CTVA' or ticker == 'DOW' or ticker == 'FOXA' or ticker =='FOX' or ticker =='HWM' or ticker == 'IR': continue
        if not os.path.exists('stocks_dfs/{}.csv'.format(ticker.replace('.', '-'))):
            df = pdr.get_data_yahoo(ticker, start, end)
            df.reset_index(inplace=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker.replace('.', '-')))
            print(ticker)
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker.replace('.', '-'), index_col=0))
        df.set_index('Date', inplace=True)
        
        
        df.rename(columns = {'Adj Close': ticker}, inplace=True)
        df.drop(['Open','High', 'Low', 'Close', 'Volume'], 1, inplace=True)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        #print(df.head(), '\n\n\n')
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.merge(df, how='outer', on='Date')
            #print(main_df.head())
        if count % 10 == 0: print(count)
      except: print('problem with {} contining iteration'.format(ticker))
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')




def visualize_data():
    df = pd.read_csv('C:\\Users\LENOVO\Desktop\sp500_joined_closes.csv', )
    df.set_index('Date', inplace=True)

    print(df.head()) 
    #Min_list = ['HWM', 'SBAC', 'NLSN', 'PYPL', 'KHC', 'VRSN', 'PAYC', 'VRSK', 'INFO', 'LB', 'APA', 'FB', 'MOS', 'GILD', 'DLR', 'SLB', 'DG', 'UA', 'NOW', 'AVGO', 'GE', 'IQV', 'COTY', 'ZTS', 'ANET', 'CPB', 'FTV', 'TWTR', 'C', 'IBM', 'LW', 'NEM', 'ABBV', 'DVN', 'CARR', 'TIF', 'UAA', 'KR', 'AIG', 'KEYS', 'TSCO', 'HRL', 'WBA', 'FLT', 'KMI', 'ADM', 'BXP', 'COP', 'CTVA',
    #            'HES', 'HFC', 'HIG', 'HST', 'JNPR', 'KSS', 'MET', 'NCLH', 'STT', 'SYF', 'TXT', 'XRX']
    
    #Max_list = ['IQV', 'INFO', 'APTV', 'CARR', 'AVY', 'VTR', 'LW', 'WAB', 'BWA', 'UA', 'DISCA', 'NWL', 'FLT', 'CHTR', 'XRAY', 'HWM', 'CTSH', 'XYL', 'TSCO', 'VIAC', 'ADS', 'UAA', 'LH', 'URI', 'CL', 'DFS', 'FTNT', 'RJF', 'T', 'KSU', 'ALGN', 'OMC', 'AXP', 'KEYS', 'HII', 'DG', 'TROW', 'HLT', 'HBI', 'DOW', 'CDW', 'GWW', 'MLM', 'MPC', 'FB', 'PEAK', 'MCK', 'AVGO',
    #            'FAST', 'ANSS', 'UHS', 'GIS', 'DLR', 'CNP', 'ALK', 'TEL', 'PAYC', 'CVS', 'CB', 'NOC', 'EMN', 'MDT', 'JBHT', 'OTIS', 'SIVB', 'BLK', 'MNST', 'DOV', 'GILD', 'DE', 'BIIB', 'PSX', 'VLO', 'V', 'OKE', 'TTWO', 'SNA', 'BKNG', 'ABC', 'UNH', 'TJX', 'CBRE', 'MO', 'PH', 'PNW', 'LIN', 'LMT', 'AZO', 'DIS', 'O', 'NOW', 'ADP', 'ITW', 'DD', 'FDX', 'CSX', 'MDLZ',
    #            'CME', 'GPC', 'IT', 'AMP', 'RTX', 'BMY', 'ODFL', 'LRCX', 'STZ', 'UNP', 'NI', 'GD', 'LNC', 'PFG', 'ORCL', 'MTB', 'EXR', 'TMO', 'MA', 'APH', 'SBAC', 'AON', 'GL', 'KO', 'LOW', 'ECL', 'KMB', 'EQIX', 'A', 'SJM', 'CERN', 'SYY', 'AME', 'AEP', 'WRB', 'ADBE', 'SYK', 'ALL', 'CBOE', 'PAYX', 'TFX', 'UDR', 'MMC', 'KLAC', 'NTRS', 'SCHW', 'COST', 'HRL', 'MSCI',
    #            'HSIC', 'FRT', 'SPG', 'MAA', 'DUK', 'ES', 'TXN', 'NEE', 'AOS', 'BKR', 'CFG', 'HUM', 'MAR', 'PNC', 'IEX', 'PPG', 'ORLY', 'FISV', 'MMM', 'MKTX', 'KEY', 'AIG', 'C', 'ROK', 'SPGI', 'MCD', 'YUM', 'XEL', 'MTD', 'WEC', 'SNPS', 'FIS', 'NKE', 'DTE', 'AMZN', 'CHD', 'ROP', 'NWS', 'NWSA', 'ANTM', 'CTAS', 'JKHY', 'CMS', 'MKC', 'DAL', 'D', 'NFLX', 'HON', 'RF',
    #            'ZION', 'ACN', 'AWK', 'MSFT', 'NSC', 'HD', 'RSG', 'DPZ', 'AMT', 'ESS', 'LNT', 'SHW', 'DISCK', 'INTU', 'MCO', 'AVB', 'EQR', 'TRV', 'WM', 'FOX', 'FOXA', 'GOOG', 'GOOGL']

    df_corr=df.corr()
    print(df_corr.head())
	
    # filter values of correlation matrix    
    #df_corr = df_corr[df_corr < -0.5]    
    #df_corr= df_corr.dropna() 

    #set diagnol zero 
    df_corr.values[[np.arange(df_corr.shape[0])]*2] = 0
    #df_corr= df_corr[df_corr != 1]
    #print(df_corr)
    
    #get and print min and max tickers
    data = df_corr.values
    min_indices = []
    min_indices = [x for _,x in sorted(zip(df_corr.min(),df_corr.idxmin()))]
    max_indices=[]
    max_indices = [x for _,x in sorted(zip(df_corr.max(),df_corr.idxmax()))]
    res_max=[]
    res_min=[]
    [res_max.append(x) for x in max_indices if x not in res_max] 
    [res_min.append(x) for x in min_indices if x not in res_min] 
    print("min correlated stocks: \n", res_min)   # sorted(df_corr.min()), min_indices, "\n\n", sorted(zip(df_corr.min(),df_corr.idxmin())), "\n\n"
    print("max correlated stocks: \n", res_max)   # sorted(df_corr.max()), max_indices, "\n\n", sorted(zip(df_corr.max(),df_corr.idxmax())), "\n\n",
    #print("\n\n\n\n\n", res_max, sorted(zip(df_corr.max(),df_corr.idxmax().drop_duplicates())))
    
    # Plot heat map
    fig = plt.figure()
    ax=fig.add_subplot(111)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[1]) + .5, minor=False)
    ax.set_yticks(np.arange(data.shape[0]) +.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index
    
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    
    #adjust color limits in accordance with filtered values
    heatmap.set_clim(-1,1)
    
    plt.tight_layout()
    plt.title("Most Positively Correlated Stocks")
    fig.savefig('sp500_corr_plot')
    plt.show()

    # adjust to just take the bottom triangle since it repeats itself

    #mask = np.zeros_like(df_corr)
    #mask[np.triu_indices_from(mask)] = True

visualize_data()