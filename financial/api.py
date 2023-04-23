from flask import Flask, jsonify, request
import mysql.connector
import time
import datetime

'''
Define variables
'''
# define data for database connection
host='db'
user='root'
password='rootpw'
database='testdb'


'''
Define functions of checking end points
'''
# check if there is any error of input of endpoint start_date and end_date 
def Endpoint_check_dates(start_date, end_date):
    try:
        # check if it's correct datetime format
        start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        #check if start_date is earlier than end_date
        if start_datetime < end_datetime:
            return False
        else:
            return True
    except:
        return True

# check if there is any error of input of symbol
def Endpoint_check_symbol(symbol):
    # symbol cannot be nothing
    if len(symbol) > 0:
        return False
    else:
        return True

# check if there is any error of input of limit
def Endpoint_check_limit(limit):
    # limit should be a positive integer
    if limit.isdigit():
        return False
    else:
        return True
    
# check if there is any error of input of endpoint page
def Endpoint_check_page(page):
    # page should be a positive integer
    if page.isdigit():
        return False
    else:
        return True


'''
Define the api services
'''
# initialize Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome! The API service is written by Hsuan-Yao Liao.'

# define financial data api
@app.route('/financial_data')
def get_financial_data():
    
    try:
        # get endpoints and set default values
        start_date = request.args.get('start_date', '2023-01-01')
        end_date = request.args.get('end_date', '2023-12-31')
        symbol = request.args.get('symbol', 'AAPL')
        limit = request.args.get('limit', '5')
        page = request.args.get('page', '1')

        # check if the input endpoints are correct
        if Endpoint_check_dates(start_date, end_date):
            raise ValueError("Start_date or end_date is in wrong format, or start_date is not earlier than end_date")
        
        if Endpoint_check_symbol(symbol):
            raise ValueError("Symbol should contain at least one char")
        
        if Endpoint_check_limit(limit):
            raise ValueError("Limit should be a positive integer")
        limit = int(limit)
        
        if Endpoint_check_page(page):
            raise ValueError("page should be a positive integer")
        page = int(page)
        
        # construct the SQL queries based on the endpoints.
        # count_query is used to count rows of data satisfied all query conditions
        # data_query is used to get the data to show in the asked pagination
        count_query = "SELECT COUNT(*) FROM financial_data"
        data_query = "SELECT * FROM financial_data"
        
        # conditions records the items of query condition in a general format
        # params records the actual parameter of each condition item
        conditions = []
        params = []

        conditions.append("symbol = %s")
        params.append(symbol)

        conditions.append("date >= %s")
        params.append(start_date)

        conditions.append("date <= %s")
        params.append(end_date)

        count_query += " WHERE " + " AND ".join(conditions)
        data_query += " WHERE " + " AND ".join(conditions)

        # create connection to database
        while True:
            try:
                cnx = mysql.connector.connect(host=host, user=user, password=password, database=database, autocommit=True)
                break
            except:
                time.sleep(1)    
        cursor = cnx.cursor()
        
        # execute the count query to get the total count of records
        cursor.execute(count_query, tuple(params))
        total_count = cursor.fetchone()[0]

        # calculate the pagination parameters
        offset = (page - 1) * limit
        total_pages = (total_count + limit - 1) // limit
        
        # if the asked page out of total page, show error to notify user
        if page > total_pages:
            raise ValueError(f"There are only {total_pages} pages, try to modify page between 1 to {total_pages}")

        # execute the data query with pagination
        data_query += " LIMIT %s OFFSET %s"
        params.append(limit)
        params.append(offset)
        cursor.execute(data_query, tuple(params))
        result = cursor.fetchall()
            
        cursor.close()
        cnx.close()
        
        # construct the response object
        response = {
            "data": result,
            "pagination": {
                "count": total_count,
                "page": page,
                "limit": limit,
                "pages": total_pages
            },
            "info": {
                "error": ""
            }
        }

    # return error if any occured
    except Exception as e:
        response = {
            "data": [],
            "pagination": {},
            "info": {
                "error": str(e)
            }
        }

    # return the response as JSON
    return jsonify(response)


# define statistics api
@app.route('/statistics')
def get_statistics():
    
    try:
        # get endpoints
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        symbol = request.args.get('symbol', '')
        
        # check if the input endpoints are correct
        if Endpoint_check_dates(start_date, end_date):
            raise ValueError("Start_date or end_date is in wrong format, or start_date is not earlier than end_date")
        
        if Endpoint_check_symbol(symbol):
            raise ValueError("Symbol should contain at least one char")

        # construct the SQL query based on the endpoints
        query = "SELECT symbol, AVG(open_price), AVG(close_price), AVG(volume) FROM financial_data WHERE date >= DATE(%s) AND date <= DATE(%s) AND symbol = %s"
        
        # create connection to database
        while True:
            try:
                cnx = mysql.connector.connect(host=host, user=user, password=password, database=database, autocommit=True)
                break
            except:
                time.sleep(1)    
        cursor = cnx.cursor()
        
        # execute the query to get the statistics data
        cursor.execute(query, (start_date, end_date, symbol))
        result = cursor.fetchall()
        
        cursor.close()
        cnx.close()
        
        # construct the response object
        response = {
            "data": result,
            "info": {
                "error": ""
            }
        }
    
    except Exception as e:
        response = {
            "data": [],
            "info": {
                "error": str(e)
            }
        }
        
    # return the response as JSON
    return jsonify(response)


# run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
