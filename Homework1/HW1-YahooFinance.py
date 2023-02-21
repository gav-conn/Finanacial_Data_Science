import pandas as pd
import yfinance as yf
import mplfinance as mpf

my_student_number = 18308483

class_list = pd.read_csv("ClassList1.csv", sep=",")
ticker_name = class_list.loc[class_list["Student ID"] 
                             == my_student_number, "Assigned Ticker"].item()

yticker = yf.Ticker(ticker_name)
BA = yticker.history(period="1y")

mpf.plot(BA, type='candle', style = 'charles', 
    title='Boeing - Price (Past Year)', xlabel = 'Date', ylabel='Price ($)')