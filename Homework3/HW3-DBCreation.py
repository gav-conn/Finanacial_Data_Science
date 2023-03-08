import requests
from bs4 import BeautifulSoup
import sqlite3 as lite
import pandas as pd
import time
from numpy.random import rand
import datetime as dt

my_student_number = 18308483
class_list = pd.read_csv('ClassList1.csv', sep=',')
class_number = class_list.loc[class_list['Student ID'] == my_student_number, 'Class Number'].item()

niters = 1000 + class_number*100

BaseStr = 'https://www.larvalabs.com/cryptopunks/details/'

con = lite.connect('CryptoPunk.db')
with con:
    cur=con.cursor()
    cur.execute('''DROP TABLE IF EXISTS PunkTrades''') 
    cur.execute('''CREATE TABLE PunkTrades(TDate date, PunkID INT, TType TEXT, TFrom TEXT, TTo TEXT, TAmt INT)''')
    
    for punk in range(niters):

        PunkNo = str(punk)
        print('Processing Punk No.:' + PunkNo)
        time.sleep(2+0.5*rand())
        page = requests.get(BaseStr + PunkNo) # Getting page HTML through request
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', attrs={'class':'table'})
        rows = table.find_all('tr')

        col_order = [4, 0, 1, 2, 3]

        for row in rows:
            cols = row.find_all('td')

            if not cols: # Screen out empty rows
                continue

            cols = [ele.text.strip() for ele in cols]
            cols = [cols[i] for i in col_order]
            cols.insert(1, PunkNo) # Add PunkID variable to our list

            # Some standardization of data
            cols[0] = dt.datetime.strptime(cols[0], '%b %d, %Y').strftime('%Y-%m-%d') # Convert to usable date format
            cols[-1] = cols[-1].split('Ξ')[0].replace('<','') # Extract ETH price of transaction
            
            try:
                cur.execute('''INSERT OR IGNORE INTO PunkTrades 
                    (TDate, PunkID, TType, TFrom, TTo, TAmt) VALUES(?,?,?,?,?,?)''', cols)

            except: 
                print('DB error: row was not inserted', cols)