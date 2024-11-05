import pandas as pd
import re
import credentials
import mysql.connector
from datetime import datetime
import pymongo
import sqlalchemy
from sqlalchemy import create_engine, text
import streamlit as st

#Read text file
Log_file="E:\\Guvi Project\\Server Log Data Extraction\\mbox.txt"
f=open(Log_file)
Data=f.read()


#Fetch Email,Date from Data
Email_Pattern=r'From:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
Date_Pattern=r'Date:\s*(\w{3},?\s*\d{1,2}\s*\w{3}\s*\d{4}\s*\d{2}:\d{2}:\d{2}\s*[-+]\d{4})'


email=re.findall(Email_Pattern,Data)
date=re.findall(Date_Pattern,Data)


#Format the date
formatted_date_list=[]
for i in date:
# Parse the date string into a datetime object
    dt = datetime.strptime(i, "%a, %d %b %Y %H:%M:%S %z")

# Format the datetime object to the desired format
    formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")
    formatted_date_list.append(formatted_date)
    


#Zip the two varibale data & Convert to dictionary
DB_UploaddData=[]
for email,date in zip(email,formatted_date_list):
    DB_UploaddData.append(({'Email': email, 'Formatted_date': date}))
    

    
#MongoDb
#Mongo DB Credential 
MongoDb_Crendiential=credentials.Mongo_DB

Mongo_Username=MongoDb_Crendiential['Username']
Mongo_Password=MongoDb_Crendiential['Password']
Mongo_NewDB=MongoDb_Crendiential['MongoDB']
Mongo_Collection=MongoDb_Crendiential['Collection']


#insert email & Date data to MongoDB
# Mongo DB connection
Client=pymongo.MongoClient(f"mongodb+srv://{Mongo_Username}:{Mongo_Password}@cluster0.6saiv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") #server

newdb=Client[Mongo_NewDB]  #Database

Collection=newdb[Mongo_Collection]

Collection.insert_many(DB_UploaddData) #upload & covert data to mongoDB database


# Fetch data from MongoDB
mongo_data = list(Collection.find({}))  # Fetch all documents from the collection


# Convert the fetched data to DataFrame
#Convert Dict to Data Frame for upload Mongo Db to MySql
df = pd.DataFrame(mongo_data)



# Remove the MongoDB _id field if present
if '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)



#Fetch Data from MongoDB and to Upload in MYSQL server
# mongoDB to MYSQL DB

#MYSQL Credential

MySql_Credential=credentials.MYSQL_CREDENTIALS
password=credentials.MYSQL_CREDENTIALS

MySql_User=MySql_Credential['user']
MySql_Password=MySql_Credential['password']
MySql_DataBase=MySql_Credential['database']
MySql_Host=MySql_Credential['host']
MySql_Port=MySql_Credential['port']



# Create Engine for Upload data Mysql server
engine=sqlalchemy.create_engine(f"mysql+mysqlconnector://{MySql_User}:{MySql_Password}@{MySql_Host}:{MySql_Port}/{MySql_DataBase}")
#Mongo DB Data to MySql
df.to_sql('user_history', con=engine, if_exists='append', index=False)


"""**MYSQL Task**"""

# Establish a MySQL connection
def get_db_connection():
    return mysql.connector.connect(**password)


def fetch_data(query):
    connection=get_db_connection()
    df=pd.read_sql(query,con=engine)
    connection.close()
    return df


def display_query_result(query,title):
    st.write(f"###{title}")
    result=fetch_data(query)
    st.dataframe(result)
    
# Streamlit app UI
st.title("Server-Log-Extraction and User-History-Database-Update")

# Set the SQL mode for MySQL
with engine.connect() as conn:
    conn.execute(text("SET SESSION sql_mode = (SELECT REPLACE(@@sql_mode, 'ONLY_FULL_GROUP_BY', ''))"))
    
query1="""
      select email Email,count(email) Count from user_history
    group by email
    order by email asc;
      
"""

display_query_result(query1,"Total Number of logs for each unique email address")

query2="""
    select email,count(email) PerCount 
    from user_history
    group by email
    ORDER BY PerCount DESC
    limit 3;
    
"""
display_query_result(query2,"Top 3 Email Addresses with the Most Logs in Total")


query3="""
    SELECT DATE(formatted_date) AS log_date, COUNT(*) AS daily_log_count
    FROM user_history
    GROUP BY log_date;
"""
display_query_result(query3,"Daily Count of Logs")

query4="""
    select  email, count(distinct date(formatted_date)) distinctdays from user_history
    group by email
    having distinctdays > 1;

"""
display_query_result(query4,"Email Addresses with Logs on Multiple Distinct Days")




query5="""
    select email,HOUR(formatted_date) AS log_hour,count(email)as logCount from user_history
    group by email, hour(formatted_date);

"""
display_query_result(query5,"Count of Logs for Each Email Address, Grouped by Hour of the Day")

query6="""
    SELECT DATE(formatted_date) AS log_date, COUNT(*) AS log_count
    FROM user_history
    GROUP BY log_date
    ORDER BY log_count DESC
    LIMIT 1;
    
"""
display_query_result(query6,"Day with the Highest Number of Logs")


query7="""
    SELECT email, 
        MIN(formatted_date) AS earliest_log, 
        MAX(formatted_date) AS latest_log
    FROM user_history
    GROUP BY email
    ORDER BY email ASC;
    
"""

display_query_result(query7,"Earliest and Latest Log Timestamp for Each Email Address")

query8="""
    select DATE(formatted_date) AS log_date, count(distinct email)  
    from user_history
    group by log_date;
    
"""
display_query_result(query8,"Count of Unique Email Addresses Logging Data on Each Day")


query9="""
    SELECT DISTINCT email,formatted_date
    FROM user_history
    WHERE DATE_FORMAT(formatted_date, '%M %e %Y') = 'January 4 2008'
    order by email asc;
    
"""

display_query_result(query9,"Email Addresses with Logs on January 4, 2008")



query10="""
    SELECT round(AVG(log_count))  AS average_logs_per_day
    FROM (
        SELECT DATE(formatted_date) AS log_date, COUNT(*) AS log_count
        FROM user_history
        GROUP BY log_date
    ) AS daily_logs;
    
"""

display_query_result(query10,"Average Number of Logs per Day")

