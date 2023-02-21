import numpy as np
import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

student_number = 18308483
class_list = pd.read_csv("ClassList1.csv", sep=",",)

ticker_name = class_list.loc[class_list["Student ID"] == student_number, "Assigned Ticker"].item()
yticker = yf.Ticker(ticker_name)

BA = yticker.history(period="1y")
SPX = yf.Ticker('SPY').history(period="1y")

# Calculate log returns
BA['Log Return'] = np.log(BA['Close'].pct_change()+1)
SPX['Log Return'] = np.log(SPX['Close'].pct_change()+1)

# Scatter plot
# fitted = np.polyfit(SPX['Log Return'].iloc[2:], BA['Log Return'].iloc[2:], 1)
# trend_line = np.poly1d(fitted)

# plt.scatter(SPX['Log Return'], BA['Log Return'], alpha=0.5)
# plt.plot(SPX['Log Return'], trend_line(SPX['Log Return']))

# plt.xlabel("Log Return on Market")
# plt.ylabel("Log Return on Boeing")
# plt.title("Log Boeing Return vs. Log Market Return")
# plt.show()

# # Histogram
# n, bins, patches = plt.hist(x=BA['Log Return'], bins='auto', color='b',
#                             alpha=0.75, rwidth=0.85)
# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('Distribution of Log Returns on Boeing')
# plt.show()

# # Box plot
# box_data = [SPX["Log Return"].values[2:], BA["Log Return"].values[2:]]

# plt.boxplot(box_data)
# plt.xticks([1, 2], ['S&P 500', 'Boeing'])
# plt.ylabel("Log Return")
# plt.show()

# Moving average
BA["Price MA 15"] = BA["Close"].rolling(window = 15, min_periods = 1).mean()
BA["Price MA 40"] = BA["Close"].rolling(window = 40, min_periods = 1).mean()

BA['Position'] = 0
BA['Position'].loc[BA["Price MA 15"]>BA["Price MA 40"]] = 1 

print(BA["Position"])
# plt.plot(BA["Close"], )
# plt.plot(BA["Price MA 15"])
# plt.plot(BA["Price MA 40"])
# plt.show()
