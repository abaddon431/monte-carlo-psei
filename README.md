# Random Walk - Monte Carlo simulation of the Philippine Stock Exchange Index

This Django web app aims to simulate and estimate the future stock market value of the Philippine Stock Exchange Index using the Random walk method and Monte Carlo simulation. this app assumes that the returns of the stock portfolio follows a normal distribution, this app also assumes that the volatility risk of the stock will not change and will remain constant

## Requirements
* [yfinance](https://pypi.org/project/yfinance/)
* [pandas](https://pypi.org/project/pandas/)
* [numpy](https://numpy.org/)
* [matplotlib](https://matplotlib.org/)

It is recommended to use [Pycharm](https://www.jetbrains.com/pycharm/) as your IDE. [Python 3](https://www.python.org/downloads/) is also the preferred version for this application
#
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages

```bash
pip install yfinance pandas numpy matplotlib
```
## Installation
1. Clone this repository
2. Open this repository on Pycharm.
3. PyCharm -> Preferences... -> Django, Enable Django Support and then choose your Django project root, settings file and manage script. (This will be subject to change).

## Variables
#### Daily Volatility
 We need to get the Daily Volatility in order to generate our random numbers for our monte carlo simulation. To do that, we first need to get our **stock_returns** by calculating the percentage change between all of the values on our data set.
```python
stock_returns = stock_data['Adj Close'].pct_change()
```
After getting our stock_returns, we can then calculate the total daily volatility by getting the standard deviation of the **stock_returns**.
```python
daily_volatility = stock_returns.std()
```
#### Random Numbers
We can then use our **daily_volatily** to generate random numbers with numpy's **random.normal()** function. This function essentially generate random numbers that will eventually create a normal (gaussian) distribution.
```python
price = prices[counter] * (1 + np.random.normal(0, daily_volatility))
```
#### Estimations
After plotting all of our data sets the we generated randomly, we can then create estimations by using the *mean* of the data set to get **estimated price**, *5th percentile* to get the **low estimate** and *95th percentile* to get the **high estimate**
```python
expected_price = np.mean(last_prices)
quantile_five = np.percentile(last_prices, 5)
quantile_ninetyfive = np.percentile(last_prices, 95)
```
# Input - Process - Output
* **Input**
  * Historical data of the stock portfolio
  * Daily Volatility of the stock
  * Trading days
  * Number of Simulations
  * Investment
* **Process**
  * Monte Carlo simulation using random walk model
* **Output**
   * Monte Carlo normal distribution chart
   * Estimations
     - Estimated Price
     - 5th percentile (5% low)
     - 95th percentile (5% high)
     - Possible gains/losses of invesment

## Technical Background
     - This section is under construction -
## Contributors
[Bryan Kenneth Tabares](https://github.com/abaddon431/)

[Mike Jerrson Galindez](https://github.com/miker-bice/).
