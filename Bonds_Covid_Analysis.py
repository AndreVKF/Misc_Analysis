from API_BBG import *
from SQL_Server_Connection import SQL_Server_Connection

Base_Date_Bonds = 20200601

EndDate=20200609
IniDate=20190101

SQL_Server_Connection = SQL_Server_Connection(database='Bonds_DB')

Query=f"""
    SELECT 
	Refdate
	,Product
	,Monitor.ISIN
	,Outstanding
	,Products.Cpn
	,Px_Mid
	,Yield
	,Z_Spread
FROM 
	Monitor 
LEFT JOIN Products ON Products.Id=Monitor.Id_Product
-- Bonds Basket
WHERE 
	Refdate>='{IniDate}' AND Refdate<='{EndDate}'
	AND Monitor.Id_Currency=1
	AND Products.Id_SecurityType=1
	AND Id_Product IN (SELECT 
	Monitor.Id_Product
FROM 
	Monitor 
LEFT JOIN Products ON Products.Id=Monitor.Id_Product
LEFT JOIN PM.dbo.Countries AS Countries ON Countries.Name=Monitor.Country
LEFT JOIN PM.dbo.Region AS Region ON Countries.Id_Region=Region.Id
WHERE 
	Monitor.Refdate='{Base_Date_Bonds}'
	AND Monitor.Id_Currency=1
	AND Products.Id_SecurityType=1
	AND Duration>=2
	AND Industry_Group NOT IN ('Sovereign')
	AND Region.Id IN (6, 3)
	AND Countries.Name NOT IN ('United States', 'Canada', 'Cayman Islands', 'Bermuda', 'Argentina')
	AND Monitor.Px_Mid>30
	AND Monitor.Riskfactor_Name NOT IN ('BONO GAR PROV DEL CHUBUT','CITY OF BUENOS AIRES','PROV OF TIERRA DEL FUEGO','PROVINCE OF NEUQUEN','PROVINCIA DE CORDOBA','PROVINCIA DE ENTRE RIOS','PROVINCIA DE RIO NEGRO','RIO ENERGY SA/UGEN SA','ODEBRECHT FINANCE LTD'))
	AND Monitor.Rtg_Group >=4 AND Monitor.Rtg_Group <=13.3
ORDER BY
	Refdate"""

Main_DF = SQL_Server_Connection.getData(query=Query, dtparse=['Refdate'])

Ret_DF = Main_DF.groupby(['Refdate']).apply(lambda x: pd.Series(sum(x.Px_Mid*x.Outstanding)/sum(x.Outstanding)))
Ret_DF.rename(columns={0: 'Price Mid'}, inplace=True)

Ret_DF['YTM'] = Main_DF.groupby(['Refdate']).apply(lambda x: pd.Series(sum((1 + x.Yield/100) * x.Outstanding)/sum(x.Outstanding)-1) * 100)
Ret_DF['Currenty Yield'] = Main_DF.groupby(['Refdate']).apply(lambda x: pd.Series(sum((1 + (x.Cpn/x.Px_Mid))*x.Outstanding)/sum(x.Outstanding)-1)*100)

Ret_DF['Z_Spread'] = Main_DF.groupby(['Refdate']).apply(lambda x: pd.Series(sum((1 + x.Z_Spread/100) * x.Outstanding)/sum(x.Outstanding)-1) * 100)

Ret_DF.to_csv(f'C:\\Users\\andre\\Documents\\Python\\Analysis\\csv\\{EndDate}-Px_Index.csv')

