# Finances
Rudimentary financial analysis, portfolio generation, and predictions. Python

This is a collection of exploratory research in stock analysis, the scripts are made to be malleable.

stonks.py is a simple candlestick plot of a given stock, moreStonks.py visualizes the S&P 500 with a correlation heatmap and has a ml prediction algorithm based on 7 day percent change with low accuracy, where max_min_corr.py adjusts moreStonks correlation map for generating portfolios of positively and negatively correlated stocks for later analysis of clustering into industries and creating hedging portfolios. 

quick_stonks.py uses autocorrelation on weekly and daily time scales for a given stock to tell you if it is momentum bound with its current trend or mean inverted meaning it might change trajectory, further statistical analysis is needed to provide significance of measure. This code is adjusted slightly to do higher frequency analysis and should be later combined with moreStonks ml algorithm and retest algorithms accuracy with larger feature vectors. 


# Class Projects 
There are two .Rmd files that are compatable with Rstudio, Quant_1.Rmd using 3 US index funds takes the absolute value of the change rate divided by the open for a day called the delta rate, and graphed verses the trading volume for each index with a linear regression model applied. 

The Beta Return file with companies from several indexes, uses an averaged beta value as a measure of synchronicity by covariance matrix between stocks, finding optimal solution with beta value then measure rate of return and its relationship between time holding for our combination and generate a portfolio of the 15 greatest highest resturning and beta valued stocks. 

