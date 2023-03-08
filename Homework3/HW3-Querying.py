import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt

sqliteConnection = lite.connect('CryptoPunk.db')
cursor = sqliteConnection.cursor()

query_price = """SELECT PunkID, max(TAmt) MaxPrice
            FROM PunkTrades
            WHERE TAmt <> '' AND TType == 'Sold'
            """

df_price_query = pd.read_sql_query(query_price, sqliteConnection)
print(df_price_query.to_latex(index=False))  

query_volume = """SELECT PunkID, COUNT(TType) NumberOfTrades
            FROM PunkTrades
            WHERE TType == 'Sold' OR TType =='Transfer' OR TType == 'Claimed'
            GROUP BY PunkID
            ORDER BY NumberOfTrades DESC
            LIMIT 5
            """

df_volume_query = pd.read_sql_query(query_volume, sqliteConnection)
print(df_volume_query.to_latex(index=False))

df_volume_query = pd.read_sql_query(query_volume, sqliteConnection)
print(df_volume_query.to_latex(index=False))

query_avg_price = """SELECT TDate, AVG(TAmt) AveragePrice
            FROM PunkTrades
            WHERE TType == 'Sold'
            GROUP BY TDate
            ORDER BY TDate ASC
            """

df_avg_price_query = pd.read_sql_query(query_avg_price, sqliteConnection)
df_avg_price_query['TDate'] = pd.to_datetime(df_avg_price_query['TDate'], format="%Y-%m-%d")
df_avg_price_query['TDate'] = df_avg_price_query['TDate'].dt.strftime("%d/%m/%Y")
df_avg_price_query.set_index("TDate", inplace=True)

ax = df_avg_price_query.plot(kind='bar', legend=False, colormap='viridis')
plt.xlabel("Date of Trade")
plt.ylabel("Average Trading Price of CryptoPunks")
plt.grid(axis='y', alpha=0.75)
plt.subplots_adjust(bottom=0.25)

[label.set_visible(False) for (i,label) in enumerate(ax.xaxis.get_ticklabels()) if i % 90 != 0]
[tick.set_visible(False) for (i,tick) in enumerate(ax.xaxis.get_ticklines()) if i % 90 != 0]

plt.show()

query_portfolio = """
                ;WITH CTE AS (
                    SELECT PunkID, TTo, TAmt, ROW_NUMBER() OVER(PARTITION BY PunkID ORDER BY TDate DESC) rn
                    FROM PunkTrades
                    WHERE TType == 'Sold'
                    GROUP BY PunkID, TDate, TTo
                    ORDER BY TDate DESC
                )

                SELECT TTo Owner, SUM(TAmt) PortfolioValue
                FROM CTE
                WHERE rn = 1
                GROUP BY TTo
                ORDER BY PortfolioValue DESC
                LIMIT 5
            """

df_portfolio_query = pd.read_sql_query(query_portfolio, sqliteConnection)
print(df_portfolio_query.to_latex(index=False))