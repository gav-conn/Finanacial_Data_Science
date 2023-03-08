import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt
import seaborn as sns

sqliteConnection = lite.connect('CryptoPunk.db')
cursor = sqliteConnection.cursor()

query_price = """
            SELECT PunkID, max(TAmt) MaxPrice
            FROM PunkTrades
            WHERE TAmt <> '' AND TType == 'Sold'
            """

df_price_query = pd.read_sql_query(query_price, sqliteConnection)
print(df_price_query.to_latex(index=False))  

query_volume = """
            SELECT PunkID, COUNT(TType) NumberOfTrades
            FROM PunkTrades
            WHERE TType == 'Sold' OR TType =='Transfer' OR TType == 'Claimed'
            GROUP BY PunkID
            ORDER BY NumberOfTrades DESC
            LIMIT 1
            """

df_volume_query = pd.read_sql_query(query_volume, sqliteConnection)
print(df_volume_query.to_latex(index=False))

query_avg_price = """
            SELECT TDate, COUNT(TAmt) NumTrades, AVG(TAmt) AveragePrice
            FROM PunkTrades
            WHERE TType == 'Sold'
            GROUP BY TDate
            ORDER BY TDate ASC
            """

df_avg_price_query = pd.read_sql_query(query_avg_price, sqliteConnection)
df_avg_price_query['TDate'] = pd.to_datetime(df_avg_price_query['TDate'], format="%Y-%m-%d")
df_avg_price_query['TDate'] = df_avg_price_query['TDate'].dt.strftime("%d/%m/%Y")
df_avg_price_query.set_index("TDate", inplace=True)

# ax = df_avg_price_query.plot(kind='bar', legend=False, colormap='viridis')
ax = sns.scatterplot(data=df_avg_price_query, x="TDate", y="AveragePrice", size="NumTrades", 
                palette='viridis', hue="NumTrades", legend=True, sizes=(15, 150), alpha=0.6)

plt.xticks(rotation='vertical')
plt.xlabel("Date of Trade")
plt.ylabel("Average Trading Price of CryptoPunks (ETH)")
plt.grid(axis='y', alpha=0.75)
plt.subplots_adjust(bottom=0.2)

leg = plt.legend(title='# Trades')
for lh in leg.legendHandles: 
    lh.set_alpha(0.6)

[label.set_visible(False) for (i,label) in enumerate(ax.xaxis.get_ticklabels()) if i % 90 != 0]
[tick.set_visible(False) for (i,tick) in enumerate(ax.xaxis.get_ticklines()) if i % 90 != 0]

plt.show()

query_portfolio = """
                ;WITH PunkTrades_Ordered AS (
                    SELECT PunkID, TType, TTo, TAmt, ROW_NUMBER() OVER(PARTITION BY PunkID ORDER BY TDate DESC) RowNum
                    FROM PunkTrades
                    WHERE TType == 'Sold' OR TType == 'Transfer'
                    GROUP BY PunkID, TDate, TTo
                    ORDER BY TDate DESC
                ),

                MostRecentSalePrice AS (
                    SELECT PunkID, min(RowNum) RecentIndex, TAmt SalePrice
                    FROM PunkTrades_Ordered
                    WHERE TType == 'Sold'
                    GROUP BY PunkID
                    ORDER BY RowNum
                )

                SELECT A.TTo Owner, SUM(B.SalePrice) PortfolioValue 
                FROM PunkTrades_Ordered A
                LEFT JOIN MostRecentSalePrice B
                ON A.PunkID == B.PunkID
                WHERE RowNum == 1
                GROUP BY Owner
                ORDER BY PortfolioValue DESC
                LIMIT 5
            """

df_portfolio_query = pd.read_sql_query(query_portfolio, sqliteConnection)
print(df_portfolio_query.to_latex(index=False))