from SQL_Server_Connection import SQL_Server_Connection
from API_BBG import *

import numpy as np

SQL_Server_Connection = SQL_Server_Connection(database='PM')
IniDate = 20200102
EndDate = 20200623

query = f"""
DECLARE @IniDate DATE
DECLARE @EndDate DATE
DECLARE @Entity NVARCHAR (255)

SET @IniDate='{IniDate}'
SET @EndDate='{EndDate}'
SET @Entity='Octante Crédito Privado FIM'

SELECT
	Position.Refdate
	,ProdId
	,Position.Ccy AS Currency
	,Position.Product
	,Position.TdPrice
	,CASE
		WHEN Position.ProdId = 1288 THEN Bonds.Cpn
		WHEN Position.ProdId = 6305 THEN 6.75/Position.TdPrice*100
		WHEN Monitor.Yield IS NULL THEN Bonds.Cpn/Position.TdPrice*100
		ELSE Monitor.Yield
	END AS Yield
	,CASE
		WHEN Position.ProdId = 6305 THEN 6.75
		ELSE Bonds.Cpn
	END AS Cpn
	,Daily_Bonds_Portfolio_NAV.Bond_Portfolio AS Bond_Portfolio_NAV
	,SUM(TotalDelta2$) AS Position_TotalDelta2
FROM
	Position
LEFT JOIN Products ON Position.ProdId=Products.Id
LEFT JOIN Bonds_DB.dbo.Products AS Bonds ON Bonds.ISIN=Products.ISIN
LEFT JOIN Bonds_DB.dbo.Monitor AS Monitor ON Monitor.Refdate=Position.Refdate 
	AND Monitor.Id_Product=Bonds.Id
LEFT JOIN (SELECT 
	Refdate
	,SUM(TotalDelta2$) AS Bond_Portfolio
FROM 
	Position 
WHERE 
	Position.Refdate>=@IniDate
	AND Position.Refdate<=@EndDate 
	AND Entity=@Entity 
	AND Instrument IN ('Corp Bond', 'Govt Bond')
GROUP BY
	Refdate) AS Daily_Bonds_Portfolio_NAV
ON Daily_Bonds_Portfolio_NAV.Refdate=Position.Refdate

WHERE
	Position.Refdate>=@IniDate
	AND Position.Refdate<=@EndDate
	AND Entity=@Entity
	AND Instrument IN ('Corp Bond', 'Govt Bond')
GROUP BY
	Position.Refdate
	,ProdId
	,Position.Product
	,Position.TdPrice
	,Monitor.Yield
	,Bonds.Cpn
	,Position.Ccy
	,Daily_Bonds_Portfolio_NAV.Bond_Portfolio
HAVING
	SUM(TotalDelta2$) <> 0"""


Main_DF = SQL_Server_Connection.getData(query=query, dtparse=['Refdate'])

# Check for Null Values
Main_DF.isnull().sum()
Main_DF['CYield'] = Main_DF['Cpn']/Main_DF['TdPrice']*100

Main_DF['Yield'] = Main_DF['Yield']/100
Main_DF['CYield'] = Main_DF['CYield']/100

# Adjust for EUR Bonds
Main_DF['Yield'] = np.where(Main_DF['Currency']=='EUR', (1+Main_DF['Yield'])*(1+1/100)-1, Main_DF['Yield'])
Main_DF['CYield'] = np.where(Main_DF['Currency']=='EUR', (1+Main_DF['CYield'])*(1+1/100)-1, Main_DF['CYield'])

# Adjust for Products
Main_DF['Prod_Yield'] = Main_DF['Yield']*Main_DF['Position_TotalDelta2']/Main_DF['Bond_Portfolio_NAV']
Main_DF['Prod_CYield'] = Main_DF['CYield']*Main_DF['Position_TotalDelta2']/Main_DF['Bond_Portfolio_NAV']

Bond_Portfolio_Yield = Main_DF.groupby(['Refdate']).agg({'Prod_Yield':'sum','Prod_CYield':'sum'})

# Nivel do Cupom Cambial
CupomCambial_DF = pd.read_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\csv\\2020-06-24 - Cupom_Cambial.csv', sep=';')
CupomCambial_DF['Refdate'] = pd.to_datetime(CupomCambial_DF['Refdate'], format='%d/%m/%Y')
CupomCambial_DF['Cupom_Cambial'] = CupomCambial_DF['Cupom_Cambial']/100

# Merge with Cupom Cambial
Bond_Portfolio_Yield = Bond_Portfolio_Yield.merge(CupomCambial_DF, how='left', on='Refdate')

# CDI+
Bond_Portfolio_Yield['CDI+ Yield'] = (1 + Bond_Portfolio_Yield['Prod_Yield'])/(1 + Bond_Portfolio_Yield['Cupom_Cambial']) - 1
Bond_Portfolio_Yield['CDI+ CYield'] = (1 + Bond_Portfolio_Yield['Prod_CYield'])/(1 + Bond_Portfolio_Yield['Cupom_Cambial']) - 1


Bond_Portfolio_Yield.to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\csv\\Bond_Portfolio_Yield_CDIMais.csv')