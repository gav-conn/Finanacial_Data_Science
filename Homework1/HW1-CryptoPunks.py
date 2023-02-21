import pandas as pd
import requests
from bs4 import BeautifulSoup

my_student_number = 18308483
BaseStr = "https://www.larvalabs.com/cryptopunks/details/"

class_list = pd.read_csv("ClassList1.csv", sep=",")
class_number = class_list.loc[class_list["Student ID"] == my_student_number, "Class Number"].item()

page = requests.get(BaseStr + str(class_number))
soup = BeautifulSoup(page.content, 'html.parser')

result_set = soup.find_all("div", class_="col-md-4")
attributes = []

for link in result_set:
    attributes.extend(link.find('a'))

attributes = attributes[1:]
print(attributes)