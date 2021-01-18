# Finances
Rudimentary financial analysis, portfolio generation, and predictions. Python

This is a collection of exploratory research in stock analysis, the scripts are made to be malleable.

stonks.py is a simple candlestick plot of a given stock, moreStonks.py visualizes the S&P 500 with a correlation heatmap and has a ml prediction algorithm based on 7 day percent change with low accuracy, where max_min_corr.py adjusts moreStonks correlation map for generating portfolios of positively and negatively correlated stocks for later analysis of clustering into industries and creating hedging portfolios. 

quick_stonks.py uses autocorrelation on weekly and daiy time scales for a given stock to tell you if it is momentum bound with its current trend or mean inverted meaning it might change trajectory, further statistical analysis is needed to provide significance of measure. This code is adjusted slightly to do higher frequency analysis and should be later combined with moreStonks ml algorithm and retest algorithms accuracy with larger feature vectors. 
