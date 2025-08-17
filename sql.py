import sqlalchemy as db
from sqlalchemy import create_engine, text
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, time

load_dotenv()
server = os.getenv("SERVER")
database = os.getenv("DATABASE")
driver = os.getenv("DRIVER")
username = os.getenv("USERNAME_SQL")
password = os.getenv("PASSWORD")


# Use a completely different connection string format for Windows Authentication
connection_string_for_odbc = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=Yes;"
DATABASE_CONNECTION = f'mssql+pyodbc:///?odbc_connect={connection_string_for_odbc}'

#DATABASE_CONNECTION = f'mssql://{username}:{password}@{server}/{database}?driver={driver}'


# Using SqlAlchemy we're starting the connection
engine = db.create_engine(DATABASE_CONNECTION)
connection = engine.connect()
metadata = db.MetaData()
schedule = db.Table('schedule', metadata, autoload_with=engine)

def check_dates(d, candidate_preferece = False):
    '''
    datetime.strftime(datetime.today(),'%Y-%m-%dT%H:%M:%SZ')

    if candidate_preferece:
        delta = timedelta(days=0)
    else:
        delta = timedelta(days=1)
    
    d = datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ')
    d = datetime.strftime(d, "%Y-%m-%d")
    '''
    schedule = db.Table('schedule', metadata, autoload_with=engine)
    query = db.select(schedule).where(schedule.columns.date == d, schedule.columns.position == 'Python Dev')
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchmany(3)
    
    if len(ResultSet) == 0:
        ResultSet = [[0, d, time(9,0,0)],[0, d, time(10,0,0)],[0, d, time(11,0,0)]] 
    
    return [
        f"{ResultSet[0][1]} {ResultSet[0][2]}",
        f"{ResultSet[1][1]} {ResultSet[1][2]}",
        f"{ResultSet[2][1]} {ResultSet[2][2]}"
    ]