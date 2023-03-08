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

# Histogram
n, bins, patches = plt.hist(x=BA['Log Return'], bins='auto', color='b',
                            alpha=0.6, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Distribution of Log Returns on Boeing')
plt.show()