from API_BBG import API_BBG
from SQL_Server_Connection import SQL_Server_Connection

import pandas as pd
import numpy as np

SQL_Server_Connection = SQL_Server_Connection(database='PM')
API_BBG = API_BBG()

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


YAS_RISK_BBG = API_BBG.BBG_POST(bbg_request='BDP', tickers=['USP190B2KG96@BGN Corp'], fields=['YAS_RISK'], overrides={"YAS_YLD_FLAG": "15", "SETTLE_DT": "20201028"})

########################################################################################

SQL_Server_Connection = SQL_Server_Connection(database='PM')

query = f"""
    SELECT
        Refdate
        ,Px_Mid FROM 
    Bonds_DB.dbo.Monitor 
        WHERE 
    Id_Product=194 
        ORDER BY 
    Refdate"""

BZ_47 = SQL_Server_Connection.getData(query=query, dtparse=['Refdate'])
BZ_47.set_index(['Refdate'], inplace=True)

slope = pd.Series(np.gradient(BZ_47['Px_Mid']), BZ_47.index, name='slope')
df = pd.concat([BZ_47, slope], axis=1)
df['Px_Adj'] = df['Px_Mid']-100

df[['Px_Adj', 'slope']].tail(360).plot()
df[['slope']].tail(360).plot()

df['Px_Diff'] = df['Px_Mid']-df['Px_Mid'].shift(1)

tst = pd.DataFrame(data=[1, 3, 4, 3, 3.5, 4, 4.5, 5], index=[1,2,3,4,5,6,7,8], columns=['Values'])
tst['Slope'] = np.gradient(tst['Values'])
tst['Diff'] = tst['Values'].diff()

tst.plot();