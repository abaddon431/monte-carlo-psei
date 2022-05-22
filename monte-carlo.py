import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# change this to change the data source of stock from yahoo finance
SOURCE = 'PSEI.PS'
stock_ticker = yf.Ticker('PSEI.PS')
stock_company = stock_ticker.info['shortName']

# code to get the data from yahoo finance using yfinance API, supplying the stock name, start date, and end date
# datetime(year,month,day)
start = dt.datetime(2021, 5, 19)
end = dt.datetime(2022, 5, 19)
stock_data = yf.download(SOURCE, start, end)

# we get stock returns by comparing the percent change of current day price to the previous day price of..
# .. adjusted close prices
stock_returns = stock_data['Adj Close'].pct_change()
# standard deviation of the stock returns
daily_volatility = stock_returns.std()

# setting of initial variables needed
trading_days = 31
last_prices = []  # last price array
last_price = stock_data['Adj Close'][-1]  # set initial value of the last price

TOTAL_SIMULATIONS = 1000
df = pd.DataFrame()
for x in range(TOTAL_SIMULATIONS):
    counter = 0
    prices = []
    # we get the simulated price by drawing random samples from a normal distribution using numpy where..
    # .. mean =0 , standard deviation = daily_volatility, ..
    # .. and multiplying the sample with the last price on the list.
    price = last_price * (1 + np.random.normal(0, daily_volatility))
    prices.append(price)

    for y in range(trading_days):
        if counter > trading_days - 1:
            break
        # this code also gets the simulated price using the same method but multiplies the random normal distribution
        # sample with the elements on the prices array
        price = prices[counter] * (1 + np.random.normal(0, daily_volatility))
        prices.append(price)
        counter += 1

    df[x] = prices
    last_prices.append(prices[-1])

# this is used for setting the plot
plt.style.use('ggplot')
fig = plt.figure()
title = str(TOTAL_SIMULATIONS) + " Monte Carlo simulations of :\n" + str(stock_company) + "for " + str(
    trading_days) + " days"
fig.suptitle(title)
fig.set_figwidth(8)
fig.set_figheight(5)
plt.plot(df)
plt.xlabel('Days')
plt.ylabel('Price')
filename = str(TOTAL_SIMULATIONS) + "-" + str(trading_days) + ".png"
plt.savefig(filename, dpi=300)
plt.show()

tickers = [SOURCE]
for ticker in tickers:
    ticker_yahoo = yf.Ticker(ticker)
    data = ticker_yahoo.history()
    last_quote = data['Close'].iloc[-1]

expected_price = np.mean(last_prices)
quantile_five = np.percentile(last_prices, 5)
quantile_ninetyfive = np.percentile(last_prices, 95)

print("Current price: ", last_quote)
print("Expected price: ", expected_price)
print("Quantile (5%): ", quantile_five)
print("Quantile (95%): ", quantile_ninetyfive)


# this is to plot the second graph
plt.hist(last_prices, bins=100)
plt.axvline(np.percentile(last_prices, 5), color='r', linestyle='dashed', linewidth=2)
plt.axvline(np.percentile(last_prices, 95), color='r', linestyle='dashed', linewidth=2)
plt.show()
