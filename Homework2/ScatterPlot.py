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

# Fit trend line
fitted = np.polyfit(SPY['Log Return'].iloc[2:], BA['Log Return'].iloc[2:], 1)
trend_line = np.poly1d(fitted)

# Plot results
plt.scatter(SPY['Log Return'], BA['Log Return'], alpha=0.5)
plt.plot(SPY['Log Return'], trend_line(SPY['Log Return']))

plt.xlabel("Log Return on Market")
plt.ylabel("Log Return on Boeing")
plt.title("Log Boeing Return vs. Log Market Return")
plt.show()