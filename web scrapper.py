import requests                 # from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager # driver
import time
from datetime import datetime
import sqlite3

url = 'https://www.cnbc.com/dow-30/'

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-crash-reporter")
options.add_argument("--disable-extensions")
options.add_argument("--disable-in-process-stack-traces")
options.add_argument("--disable-logging")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")
options.add_argument("--output=/dev/null")

driver = webdriver.Edge(options=options, service=Service(EdgeChromiumDriverManager().install()))
driver.maximize_window()
driver.get(url)

time.sleep(5) # take a pause 10 seconds

html = driver.page_source

# Close the WebDriver
driver.close()
driver.quit()


# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

tableHeadThs = soup.select('.BasicTable-tableHeading > tr > th')

columns = ['[' + '_'.join(th.span.text.split(' ')[:-1]).lower() + ']' for th in tableHeadThs]

print(columns)
rows = []

if (len(columns) > 0):
    tableBodyTrs = soup.select('.BasicTable-tableBody > tr')
    if (len(tableBodyTrs) > 0):
        for tr in tableBodyTrs:            
            tr_children = list(tr.children)            
            if (len(columns) == len(tr_children)):
                row = {}
                for i in range(0, len(tr_children)):                
                    child = tr_children[i]
                    child_text = child.text.replace(',', '.')                                
                    row[columns[i]] = float(child_text) if ('BasicTable-numData' in child['class']) else child_text                                                    
                row['datetime'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                rows.append(row)
            else:  
                print('columns and tr has different lens')            
    else:
        print('empty tableBodyTrs ')
else:
    print('empty columns')

conexion = sqlite3.connect('stock.db')
cursor = conexion.cursor()

# CREA TABLA
cursor.execute(
'''
CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol          TEXT,
    name            TEXT,
    price           REAL,
    change          TEXT,
    [%change]       TEXT,
    low             REAL,
    high            REAL,
    previous_close  REAL,
    datetime        TEXT
)
''')


if (len(rows) > 0):
    for row in rows:        
        columns_query = []
        values_query = []
        for (key, value) in row.items():
            columns_query.append(key)
            values_query.append(str(value) if type(1.0) == type(value) else "'" + str(value) + "'")        
        insert_query = f'''INSERT INTO stock ({",".join(columns_query)}) values ({', '.join(values_query)})'''
        print(insert_query)
        cursor.execute(insert_query)
else:
    print('no rows')

conexion.commit()

# select
#cursor.execute('SELECT * FROM stock;')
#rows = cursor.fetchall()
#for row in rows:
#    print(row)

cursor.close()
conexion.close()