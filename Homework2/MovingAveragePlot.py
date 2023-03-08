import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

student_number = 18308483
class_list = pd.read_csv("ClassList1.csv", sep=",")

ticker_name = class_list.loc[class_list["Student ID"] == student_number, "Assigned Ticker"].item()
yticker = yf.Ticker(ticker_name)

BA = yticker.history(period="1y")
SPY = yf.Ticker('SPY').history(period="1y")

# Calculate log returns
BA['Log Return'] = np.log(BA['Close'].pct_change()+1)
SPY['Log Return'] = np.log(SPY['Close'].pct_change()+1)

# Moving average
BA["Price MA 15"] = BA["Close"].rolling(window = 15, min_periods = 1).mean()
BA["Position"] = (BA["Price MA 15"] - BA["Close"]).apply(np.sign)
BA["Change in Position"] = (BA["Position"]-BA["Position"].shift(-1)).apply(np.sign)
BA.iloc[0,-1] = 0

# Plot Closing Price & MA
plt.plot(BA["Close"], label = 'Closing Price of Boeing', color = '#404040')
plt.plot(BA["Price MA 15"], label = "Moving Average (15-day)", color = '#15b0b0')

# Plot Buy/Sell Markers
plt.plot(BA[BA['Change in Position'] == 1].index, 
         BA["Price MA 15"][BA['Change in Position'] == 1], 
         'v', markersize = 10, color = '#0d5c2f', label = 'Buy')
plt.plot(BA[BA['Change in Position'] == -1].index, 
         BA["Price MA 15"][BA['Change in Position'] == -1], 
         'v', markersize = 10, color = '#b01515', label = 'Sell')

plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.legend()
plt.show()