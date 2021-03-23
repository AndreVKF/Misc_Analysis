import pandas as pd
import numpy as np

from SQL_Server_Connection import SQL_Server_Connection

iniDate = 20190903
PM_Connection = SQL_Server_Connection(database='PM')

Query = f"""
SELECT 
	Trades.Id AS Id
	,TradeDate AS TradeDate
	,Entities.Name AS Entity
	,Products.Name AS Product
	,Quantity AS Quantity
	,Trades.Price AS Price
	,Dealers.Name AS Dealer
	,Trades.Value AS Value
	,Trades.Settlement AS Settlement
	,CASE
		WHEN Id_Instrument=45 THEN 'Corp Bond'
		WHEN Products.Id_RiskFactor1=104 THEN 'US TBill'
		ELSE 'Govt Bond'
	END AS Bond_Type
FROM 
	Trades 
LEFT JOIN Products ON Trades.Id_Product=Products.Id
LEFT JOIN Dealers ON Trades.Id_Dealer=Dealers.Id
LEFT JOIN RiskFactor ON RiskFactor.Id=Products.Id_RiskFactor1
LEFT JOIN Entities ON Entities.Id=Trades.Id_Entity
WHERE 
	TradeDate>='{iniDate}'
	AND Id_Entity IN (3)
	AND Trades.Price <> 0
	AND Id_Dealer NOT IN (97,79,76,91,50,112,119,53,113,96,51,106,111,47,121,102,98,85)
	AND Id_Instrument IN (44, 45)

"""

Trades_DF = PM_Connection.getData(query=Query, dtparse=['TradeDate', 'Settlement'])
Trades_DF = Trades_DF[['TradeDate', 'Product', 'Id', 'Dealer', 'Quantity', 'Price']]

DaysWithArb = Trades_DF.groupby(['TradeDate', 'Product']).count()
DaysWithArb[(DaysWithArb['Id']>1)].index.get_level_values(0).unique().to_list()

tst = Trades_DF.loc[(Trades_DF['TradeDate']).isin(DaysWithArb[(DaysWithArb['Id']>1)].index.get_level_values(0).unique())]

Trades_Indexed = tst.set_index(['TradeDate', 'Product'])

############################
pl = Trades_Indexed.reset_index()
pl2 = pl.groupby(['TradeDate', 'Product']).count()
pl2 = pl2.loc[(pl2['Id']>1)]

Index2 = pl2.index.to_list()


Final = Trades_DF[Trades_DF[['TradeDate', 'Product']].apply(tuple, axis=1).isin(Index2)]
Final = Final.set_index(['TradeDate', 'Product'])


excelWb = pd.ExcelWriter('C:\\Users\\andre\\Documents\\Python\\Analysis\\Excel\\OCP_Trades.xlsx', engine='xlsxwriter')
Final.to_excel(excelWb)
excelWb.save()