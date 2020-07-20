from API_BBG import BBG_POST
from SQL_Server_Connection import SQL_Server_Connection

import pandas as pd
import numpy as np

SQL_Server_Connection = SQL_Server_Connection(database='PM')

RiskFactors = SQL_Server_Connection.getData(query="SELECT * FROM Riskfactor")

########## Tickers ##########
TckBBG = ['BRL Curncy','IBOV Index','ODF25 Comdty','CBRZ1U5 CBIN Curncy']
TckBonds = BBG_POST('BDH', TckBBG, 'PX_LAST', date_start=19010101, date_end=20200514)

TckBonds.dropna(inplace=True)

TckBonds = TckBonds.merge(RiskFactors, how='left', left_on='Ticker', right_on='RiskTicker')
TckBonds.rename(columns={'Refdate': 'Date', 'Id': 'Id_RiskFactor', 'PX_LAST': 'Value'}, inplace=True)
TckBonds = TckBonds[['Date', 'Id_RiskFactor', 'Value']]

Id_List = TckBonds['Id_RiskFactor'].drop_duplicates().to_list()


for Id_RiskFactor in Id_List:
    SQL_Server_Connection.execQuery(query=f'DELETE FROM IndexesValue WHERE Id_RiskFactor={Id_RiskFactor}')

    insert_DF = TckBonds[(TckBonds['Id_RiskFactor']==Id_RiskFactor)]
    insert_DF['1DReturn'] = np.nan
    insert_DF['5DReturn'] = np.nan

    SQL_Server_Connection.insertDataFrame(tableDB='IndexesValue', df=insert_DF)
