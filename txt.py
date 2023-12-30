import datetime
import logging
import ftplib
import pyodbc
import pandas as pd
import os
import azure.functions as func
from datetime import datetime, timedelta


FTP_HOST = '145.14.156.45'
FTP_USER =  'u251061335.turntable'
FTP_PASS = 'Turntable2020.'
GPG_PASSPHRASE = 'q#HMPrDK&h4J9@J%dHbH3'

server = 'all-startup-server.database.windows.net'
database = 'MusicComponentDb'
username = 'startupadmin'
password = 'Adegoke1234#'

def previousDayFileName():
    current_date = datetime.now()
    previous_day = current_date - timedelta(days=1)
    previous_day_formatted = previous_day.strftime('%Y%m%d')
    filePath = "Boomplay_NG_"+previous_day_formatted+'.csv'
    return filePath

def ftpDownload(filename):
    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
    ftp.encoding = "utf-8"
    print('FTP - welcome ~ '+ftp.getwelcome())
    
    with open(filename, 'wb') as file:
        ftp.retrbinary(f"RETR {filename}", file.write)

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    filename = previousDayFileName()
    ftpDownload(filename)

    df = pd.read_csv(filename)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')

    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        print("Connected to the database")
    except pyodbc.Error as e:
        print(f"Error connecting to the database: {str(e)}")

    row_to_insert = df.iloc[0]
    date_to_check = row_to_insert['Date']  
    cursor.execute("SELECT COUNT(*) FROM dbo.BoomplayDailyIndividualStreams WHERE [Date] = ?", date_to_check)
    result = cursor.fetchone()

    if result[0] == 0:
        print()
    else:
        print(f"The date {date_to_check} already exists in the database.")


    logging.info('Python timer trigger function ran at %s', utc_timestamp)