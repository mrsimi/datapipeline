import pyodbc
import time
import logging

# db_server = 'servername'
# db_user = 'db_user'
# db_password = 'db_pass'
# db_dbname = 'db_name'
# db_tbl_log = 'log'

server = 'all-startup-server.database.windows.net'
database = 'MusicComponentDb'
username = 'startupadmin'
password = 'Adegoke1234#'
tablename = 'logs'

log_file_path = 'C:\\Users\\Yourname\\Desktop\\test_log.txt'
log_error_level     = 'DEBUG'       # LOG error level (file)
log_to_db = True                    # LOG to database?

class LogDBHandler(logging.Handler):
    '''
    Customized logging handler that puts logs to the database.
    pymssql required
    '''
    def __init__(self, sql_conn, sql_cursor, db_tbl_log):
        logging.Handler.__init__(self)
        self.sql_cursor = sql_cursor
        self.sql_conn = sql_conn
        self.db_tbl_log = db_tbl_log

    def emit(self, record):
        # Set current time
        tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))
        # Clear the log message so it can be put to db via sql (escape quotes)
        self.log_msg = record.msg
        self.log_msg = self.log_msg.strip()
        self.log_msg = self.log_msg.replace('\'', '\'\'')
        # Make the SQL insert
        sql = 'INSERT INTO ' + self.db_tbl_log + ' (log_level, ' + \
            'log_levelname, log, created_at, created_by) ' + \
            'VALUES (' + \
            ''   + str(record.levelno) + ', ' + \
            '\'' + str(record.levelname) + '\', ' + \
            '\'' + str(self.log_msg) + '\', ' + \
            '(convert(datetime2(7), \'' + tm + '\')), ' + \
            '\'' + str(record.name) + '\')'
        try:
            self.sql_cursor.execute(sql)
            self.sql_conn.commit()
        # If error - print it out on screen. Since DB is not working - there's
        # no point making a log about it to the database :)
        except pyodbc.Error as e:
            print (sql)
            print ('CRITICAL DB ERROR! Logging to database not possible!')

# Main settings for the database logging use
if (log_to_db):
    # Make the connection to database for the logger
    #log_conn = pymssql.connect(server, username, password, database, 30)
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    log_conn = pyodbc.connect(connection_string)
    log_cursor = log_conn.cursor()
    logdb = LogDBHandler(log_conn, log_cursor, tablename)

# Set logger
logging.basicConfig(filename=log_file_path)

# Set db handler for root logger
if (log_to_db):
    logging.getLogger('').addHandler(logdb)
# Register MY_LOGGER
log = logging.getLogger('MY_LOGGER')
log.setLevel(log_error_level)

# Example variable
test_var = 'This is test message'

def logMessthod():
    log.info("log from inside metthod")

logMessthod()

# Log the variable contents as an error
log.info('This an infor occurred: %s' % test_var)