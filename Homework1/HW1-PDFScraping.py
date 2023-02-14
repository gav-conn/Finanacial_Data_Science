import tabula as tb
import pandas as pd

gdp_lst = tb.read_pdf("GDP11.pdf", pages='1', pandas_options={'header': None})
gdp_df = pd.DataFrame(gdp_lst[0])
gdp_df.drop(columns=gdp_df.columns[-1], axis=1, inplace=True)
gdp_df.columns = ["Country", "Ranking", "Economy", "GDP"]

print(gdp_df.to_latex(index = False))