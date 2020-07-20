from API_BBG import BBG_POST
from SQL_Server_Connection import SQL_Server_Connection

yearBase = 2018

GT10 = BBG_POST(bbg_request='BDH', tickers=['GT10 Govt'], fields=['PX_LAST'], date_start=20180101, date_end=20200716)
GT10.to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\csv\\GT10.csv')