import requests
from bs4 import BeautifulSoup
import csv


r = requests.get(f"https://sis.ou.edu/ted/home/byOU?ou_subj_code=A+HI&ou_course=&stat_code=AL&sbgi_code=")
soup = BeautifulSoup(r.content.decode('utf8'),"lxml")
table = soup.find("table",{"summary":"OU matches"}) # to select the right table

# find all rows
rows = table.findAll('tr')

# strip the header from rows
headers = rows[0]
header_text = []

# add the table header text to array
for th in headers.findAll('th'):
    header_text.append(th.text)

# init row text array
row_text_array = []

# loop through rows and add row text to array
for row in rows[1:]:
    row_text = []
    # loop through the elements
    for row_element in row.findAll(['th', 'td']):
        # append the array with the elements inner text
        row_text.append(row_element.text.replace('\n', '').strip())
    # append the text array to the row text array
    row_text_array.append(row_text)

with open("out.csv", "w") as f:
    wr = csv.writer(f)
    wr.writerow(header_text)
    for row_text_single in row_text_array:
        wr.writerow(row_text_single) 