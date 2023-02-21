import pandas as pd
import yfinance as yf
import mplfinance as mpf

class_list = pd.read_csv("ClassList1.csv", sep=",")

ticker_name = class_list.loc[class_list["Student ID"] == 18308483, "Assigned Ticker"].item()
yticker = yf.Ticker(ticker_name)

BA = yticker.history(period="1y") # max, 1y, 3mo

mpf.plot(BA, type='candle', style = 'charles', 
    title='Boeing - Price (Past Year)', xlabel = 'Date', ylabel='Price ($)')