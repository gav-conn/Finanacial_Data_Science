import yfinance as yf
import pandas as pd
import datetime as dt
from matplotlib import cm
from matplotlib import pyplot as plt

# Code to pull an option chain from yahoo finance
def options_chain(symbol):

    tk = yf.Ticker(symbol)
    # Expiration dates
    exps = tk.options

    # Get options for each expiration
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        opt = pd.concat([pd.DataFrame(), opt.calls, opt.puts])
        opt['expirationDate'] = e
        options = pd.concat([options, opt], ignore_index=True)
    
    # Bizarre error in yfinance that gives the wrong expiration date
    # Add 1 day to get the correct expiration date
    options['expirationDate'] = pd.to_datetime(options['expirationDate']) + dt.timedelta(days = 1)
    options['dte'] = (options['expirationDate'] - dt.datetime.today()).dt.days 
    
    # Boolean column if the option is a CALL
    options['CALL'] = options['contractSymbol'].str[4:].apply(
        lambda x: "C" in x)
    
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['mark'] = (options['bid'] + options['ask']) / 2 # Calculate the midpoint of the bid-ask
    
    # Drop unnecessary and meaningless columns
    options = options.drop(columns = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate', 'lastPrice'])

    return options

student_number = 18308483
class_list = pd.read_csv("ClassList1.csv", sep=",")

ticker_name = class_list.loc[class_list["Student ID"] == student_number, "Assigned Ticker"].item()
yticker = yf.Ticker(ticker_name)

BA = yticker.history(period="1y")
options_data = options_chain(ticker_name)

options_data = options_data[(options_data.volume > 10) & (options_data.CALL == True)]

# generate x,y,z values
xaxis=options_data['dte'] #days to expiry
yaxis=options_data['strike']
zaxis=options_data['impliedVolatility']
fig4 = plt.figure(2)
ax = fig4.add_subplot(111, projection='3d')
ax.plot_trisurf(xaxis, yaxis, zaxis, cmap=cm.jet)    
ax.set_xlabel('Days to Expiration')
ax.set_ylabel('Strike Price')
ax.set_zlabel('Implied Volatility for Call Options')
plt.suptitle('Implied Volatility Surface for %s Current Price: %s Date: %s' %
                 (ticker_name, '{0:.4g}'.format(BA['Close'].values[-1]), dt.date.today()))

plt.show()