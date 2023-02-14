import pandas as pd
import requests
from dateutil.parser import parse
from bs4 import BeautifulSoup

class_list = pd.read_csv("ClassList1.csv", sep=",",)
class_number = class_list.loc[class_list["Student ID"] == 18308483, "Class Number"].item()

BaseStr = "https://www.larvalabs.com/cryptopunks/details/"
page = requests.get(BaseStr + str(class_number))
soup = BeautifulSoup(page.content, 'html.parser')

test = soup.find(class_="col-md-10 col-md-offset-1")
result = test.find_all('a')
print(result)
# for row in rows:
#     cols = row.find_all('td')
#     if cols:
#         cols = [ele.text.strip() for ele in cols]
#         print(cols[4] + ' : ' + cols[3])