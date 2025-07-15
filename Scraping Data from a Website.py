from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.scrapethissite.com/pages/forms/'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html')

table = soup.find_all('th')


table_title_data = [title.text.strip() for title  in table]
print(table)

df = pd.DataFrame(columns = table)

column_data = soup.find_all('td')


# Assuming 'table' contains the column names
df = pd.DataFrame(columns=table)

# Extracting rows from the HTML
rows = soup.find_all('tr')[1:]  # Skip the header row

for row in rows:
    row_data = row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]
    
    # Adjust the row length to match DataFrame columns
    adjusted_row_data = individual_row_data[:len(df.columns)] + [None] * (len(df.columns) - len(individual_row_data))
    
    # Add adjusted row to the DataFrame
    length = len(df)
    df.loc[length] = adjusted_row_data




