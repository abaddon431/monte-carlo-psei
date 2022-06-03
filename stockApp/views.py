from django.shortcuts import render, redirect
from django.contrib import messages
# imports for stocks forecasting and graph plotting
import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# Create your views here.

# this is for the home view
def home(request):
    # request.session.flush()
    # this function is responsible for current prices
    ticker_yahoo = yf.Ticker('PSEI.PS')
    data = ticker_yahoo.history()
    last_quote = data['Close'].iloc[-1]
    prev_lastquote = data['Close'].iloc[-2]
    degree = "(" + str(round(((last_quote - prev_lastquote) / abs(last_quote)) * 100, 2)) + "%)"
    change_val = round(last_quote - prev_lastquote, 2)
    change_pct = str(round(last_quote-prev_lastquote,2))+degree
    context = {
        'current_price': round(last_quote, 3),
        'change_pct': change_pct,
        'change_val': change_val
    }

    return render(request, 'stockApp/home.html', context)


def update_stock(request):
    request.session.flush()
    # this accepts the form fields
    simulation_days = int(request.POST['simulation_days'])
    simulation_number = int(request.POST['simulation_number'])
    if simulation_days == 0 or simulation_number == 0:
        messages.error(request, f'Invalid number of Days or number of Simulation')
        return redirect('stockApp:home')
    else:
        # change this to change the data source of stock from yahoo finance
        SOURCE = 'PSEI.PS'
        stock_ticker = yf.Ticker('PSEI.PS')
        stock_company = stock_ticker.info['shortName']

        # code to get the data from yahoo finance using yfinance API, supplying the stock name, start date, and end date
        # datetime(year,month,day)
        start = dt.datetime(2011, 5, 19)
        end = dt.datetime.today()
        stock_data = yf.download(SOURCE, start, end)

        # we get stock returns by comparing the percent change of current day price to the previous day price of..
        # .. adjusted close prices
        stock_returns = stock_data['Adj Close'].pct_change()
        # standard deviation of the stock returns
        daily_volatility = stock_returns.std()

        # setting of initial variables needed
        trading_days = simulation_days + 1
        last_price = stock_data['Adj Close'][-1]  # set initial value of the last price
        TOTAL_SIMULATIONS = simulation_number
        
        # further optimization of code
        # the next line creates 2 dimensional array using numpy where rows = trading days and columns = total sims
        # while generating and inserting random numbers
        # on the array based on the daily_volatility as range
        random_dataset = 1 + np.random.normal(0, daily_volatility, (trading_days, TOTAL_SIMULATIONS))
        price_list = np.zeros_like(random_dataset)  # create and populate an array shaped like the random generated array with zeroes
        price_list[0] = last_price  # initialize the origin

        # loop for calculating the simulated prices based on the previous days and the random dataset
        for x in range(1, trading_days):
            price_list[x] = price_list[x-1] * random_dataset[x]
        last_prices = price_list[simulation_days]

        # this is used for setting the plot
        plt.style.use('ggplot')
        title = str(TOTAL_SIMULATIONS) + " Monte Carlo simulations of :\n" + str(stock_company) + " for " + str(
            trading_days - 1) + " days"
        
        fig1, ax1 = plt.subplots()
        ax1.plot(price_list)
        ax1.set_title(title)
        ax1.set_ylabel("Price")
        ax1.set_xlabel("Days")

        # plt.axhline(y=last_quote, color='black', linestyle='-') # blackline
        # initialize latest price
        last_quote = stock_data['Adj Close'][-1]
        current_directory = "./static/images/graph"
        filename = "forecast_graph.png"
        plt.savefig(os.path.join(current_directory, filename), dpi=300)
        # plt.show()

        expected_price = np.mean(last_prices)
        quantile_five = np.percentile(last_prices, 5)
        quantile_ninetyfive = np.percentile(last_prices, 95)

        # this is to plot the second graph (histogram)

        fig2, ax2 = plt.subplots()
        ax2.hist(last_prices, bins=100, color='#6397ff')
        ax2.set_title(title)
        ax2.set_ylabel("Price")
        ax2.set_xlabel("Days")
        plt.axvline(np.percentile(last_prices, 5), color='r', linestyle='dashed', linewidth=2)
        plt.axvline(np.percentile(last_prices, 95), color='r', linestyle='dashed', linewidth=2)

        filename = "histogram.png"
        plt.savefig(os.path.join(current_directory, filename), dpi=300)
        # plt.show()

        # this is the session that will save the data from this function
        # del request.session['expected_price', 'quantile_five', 'quantile_ninetyfive']
        # request.session['current_price'] = round(last_quote, 2)
        request.session['expected_price'] = round(expected_price, 2)
        request.session['quantile_five'] = round(quantile_five, 2)
        request.session['quantile_ninetyfive'] = round(quantile_ninetyfive, 2)


        # in this return, redirect the users to the home template
        return redirect('stockApp:home')
    
