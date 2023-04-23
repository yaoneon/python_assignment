# Before using
Apikey for using service provided by alphavantage should be set.  
Simply copy and paste your apikey to apikey.txt(in the subfolder 'financial').


# Start using
1. Navigate to the project folder and run docker-compose up in your terminal.
2. Wait until 'Complete database settings, APIs are available now!' shows in your terminal, that means all requirements are well set up. (It typically costs fewer than 90 seconds.)
3. Input your API request in a browser to get response. Note the port of API services is set to 5000.
Usage example:'http://localhost:5000/financial_data?start_date=2023-04-11&end_date=2023-04-20&symbol=AAPL&limit=10'

*If any file is modified by yourself, run docker-compose up --build to confirm all changes are recognized by docker.


# Description of each file
## docker-compose.yml
docker-compose.yml is the first to be implemented.  
The file defines three services, which are 'db', 'setup_db' and 'api' respectively.  
-'db' is based on mysql image and would be used to build local database services. Environment variable and initialization settings of mysql are defined in this block as well.  
-'setup_db' is based on python image and depends on 'db' since it is used to create table and insert data in DB. The body of this service is defined in get_raw_data.py, which would be implemented by the default command.  
-'api' is based on python image and depends on 'setup_db' since it relies on data in the DB. The api serive is defined in financial/api.py which would be implemented by default command. The port of API service is 5000, please react with the service by port 5000.

## Dockerfile
The file creates an image used in two services: 'setup_db' and 'api'.  
It is based on a image 'python3.9-slim-buster'. All requirements mentioned in requirements.txt would be installed.

## requirements.txt
Simply defines the required modules, which would be installed when building images of two services: 'setup_db' and 'api'.

## schema.sql
Records the sql script of creating financial_data table.  
Note symbol and date are set to be primary key to avoid duplicated insert. (Will yield error and be handled by get_raw_data.py)

## apikey.txt
Records the apikey for calling alphavantage services.

## get_raw_data.py
The code will be triggered by the service 'setup_db'.  
It first creates financial_data table, then call API to get stock infos, finally organize and insert the data to financial_data table.

## api.py
The code will be triggered by the service 'api'.  
It defines the two API services which are 'financial_data' and 'statistcs'. All API requests will be handled by this code.

# Issues

## In general
To complete the tasks, techniques of python programming, database handling, docker control and data cleaning are used.  
Aim to make the service easy implementing, I well organized the codes and files. Users can easily turn on it by only entering one command 'docker-compose up'. (Of course apikey should be set first.)  
As a developer working on Windows system and never heard docker before, it's a challenge to deal with the tasks. However, I completed the mission after hard studying and gained a lot during this process. No matter if I can pass the interviews, thanks for the well-designed assignment.

## Slow DB installation
It takes relatively long time to install a DB in docker. At the beginning, I often encountered the problem of fail connection to DB. The reason is when I tried to build a connection by python, the Mysql database is always not installed yet. I put the connection process in a while loop to confirm the code will continue only if the connection is built correctly.

## Package
I used the following packages:  
1. mysql-connector: connect to DB
2. Flask: handle HTTP responses and requests
3. requests: call alphavantage API  

To improve the performance, it's better to use lighter packages.  
Although I didn't use huge packages in my perspective, there are potential improvements by replacing the packages to smaller ones if it have necessary functions as well.

