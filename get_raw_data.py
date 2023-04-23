import requests
import datetime
import time
import mysql.connector

# function to create financial_data table
def Create_financialdata_table(host, user, password, database):
    
    # create connection to database
    while True:
        try:
            cnx = mysql.connector.connect(host=host, user=user, password=password, database=database, autocommit=True)
            break
        except:
            time.sleep(1)    
    
    cursor = cnx.cursor()
    
    # create table 'financial_date' based on the sql file
    with open('schema.sql', 'r') as file:
        query = file.read()

    cursor.execute(query)
    cursor.close()
    cnx.close()

# call alphavantage api to get stock prices and organize the raw data
def Get_data_todb(symbol, apikey):
    url = f'https://www.alphavantage.co/query?&function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={apikey}'
    r = requests.get(url)
    data_raw = r.json()
    
    # get today's date
    today = datetime.date.today()

    # get the date from two weeks ago
    two_weeks_ago = today - datetime.timedelta(weeks=2)

    # create a list of dates between today and two weeks ago
    date_list = [two_weeks_ago + datetime.timedelta(days=i) for i in range((today - two_weeks_ago).days + 1)]

    # organize raw data as needed to store in database
    data_todb = list()
    for date in date_list:
         if str(date) in data_raw['Time Series (Daily)']:
             open_price = data_raw['Time Series (Daily)'][str(date)]['1. open']
             close_price = data_raw['Time Series (Daily)'][str(date)]['4. close']
             volume = data_raw['Time Series (Daily)'][str(date)]['6. volume']
             data_todb.append((symbol, date, float(open_price), float(close_price), int(volume)))
    
    return data_todb

def Insert_data_todb(data_todb, host, user, password, database): 
    sql_script = 'insert into financial_data (symbol, date, open_price, close_price, volume) values (%s, DATE(%s), %s, %s, %s)'
    
    # create connection to database
    while True:
        try:
            cnx = mysql.connector.connect(host=host, user=user, password=password, database=database, autocommit=True)
            break
        except:
            time.sleep(1)    

    cursor = cnx.cursor()
    
    # insert data to table
    for data in data_todb:
        try:
            cursor.execute(sql_script, data)
        # catch error (especially for duplicated insert)
        except Exception as e:
            print(str(e))
    
    cursor.close()
    cnx.close()

if __name__ == '__main__':
    
    # set db connection info
    host = 'db'
    user = 'root'
    password = 'rootpw'
    database = 'testdb'
    
    # create table in database
    Create_financialdata_table(host, user, password, database)
    
    # access apikey
    with open('financial/apikey.txt', 'r') as apifile:
        apikey = apifile.read
    
    # set the company symbol to retrieve stock data
    symbols = ['IBM', 'AAPL']
    
    # get and insert desired data to database
    for symbol in symbols:
        Insert_data_todb(Get_data_todb(symbol, apikey), host, user, password, database)
    
    print('---------------------------------------------------')
    print('Complete database settings, APIs are available now!')
    print('---------------------------------------------------')