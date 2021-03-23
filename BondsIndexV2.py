import pandas as pd
import numpy as np

from SQL_Server_Connection import SQL_Server_Connection

iniDate = 20200101
PM_Connection = SQL_Server_Connection(database='PM')

query = f"""
SELECT 
    Refdate
    ,Product
    ,Monitor.ISIN
    ,Monitor.Country
    ,Outstanding
    ,Products.Cpn
    ,Px_Mid
    ,Yield
    ,Z_Spread
FROM 
    Bonds_DB.dbo.Monitor AS Monitor
LEFT JOIN Bonds_DB.dbo.Products AS Products ON Products.Id=Monitor.Id_Product
LEFT JOIN Countries AS Countries ON Countries.Name=Monitor.Country
LEFT JOIN Region AS Region ON Countries.Id_Region=Region.Id
-- Bonds Basket
WHERE 
    Monitor.Id_Currency=1
    AND Products.Id_SecurityType=1
    AND Monitor.Refdate IN (SELECT Date FROM PM.dbo.IndexesValue WHERE Id_RiskFactor=734)
    AND Monitor.Refdate NOT IN ('20200224')
    AND Monitor.Outstanding >=300000
    AND Monitor.Id_Currency=1
    AND Products.Id_SecurityType=1
    AND Duration>=1
    AND Industry_Group NOT IN ('Sovereign')
    AND Region.Id IN (6, 3)
    AND Countries.Name NOT IN ('United States', 'Canada', 'Cayman Islands', 'Bermuda', 'Argentina')
    AND Monitor.Riskfactor_Name NOT IN ('BONO GAR PROV DEL CHUBUT','CITY OF BUENOS AIRES','PROV OF TIERRA DEL FUEGO','PROVINCE OF NEUQUEN','PROVINCIA DE CORDOBA','PROVINCIA DE ENTRE RIOS','PROVINCIA DE RIO NEGRO','RIO ENERGY SA/UGEN SA','ODEBRECHT FINANCE LTD')
    AND Monitor.Rtg_Group >=0 AND Monitor.Rtg_Group <=12
ORDER BY
    Refdate"""

Index_DF = PM_Connection.getData(query=query, dtparse=['Refdate'])

# Index_DF[(Index_DF['Refdate']=='20200812')].to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\csv\\Bonds.csv')

# Brazil_DF = Index_DF[(Index_DF['Country']=='Brazil')]
# Brazil_DF = Brazil_DF.groupby(['Refdate']).apply(lambda x: pd.Series(sum(x.Px_Mid*x.Outstanding)/sum(x.Outstanding)))
# Brazil_DF.rename(columns={0: 'Px_Mid'}, inplace=True)

# Brazil_DF.to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\csv\\BrasilDF.csv')

Px_DF = Index_DF.groupby(['Refdate']).apply(lambda x: pd.Series(sum(x.Px_Mid*x.Outstanding)/sum(x.Outstanding))).reset_index()
Px_DF.rename(columns={0: 'Value', 'Refdate': 'Date'}, inplace=True)

Px_DF['Id_RiskFactor'] = 734
Px_DF['1DReturn'] = np.nan
Px_DF['5DReturn'] = np.nan

Z_DF = Index_DF.groupby(['Refdate']).apply(lambda x: pd.Series(sum((1 + x.Z_Spread/100) * x.Outstanding)/sum(x.Outstanding)-1) * 100).reset_index()
Z_DF.rename(columns={0: 'Value', 'Refdate': 'Date'}, inplace=True)

Z_DF['Id_RiskFactor'] = 735
Z_DF['1DReturn'] = np.nan
Z_DF['5DReturn'] = np.nan

PM_Connection.insertDataFrame(tableDB='IndexesValue', df=Px_DF[['Date', 'Id_RiskFactor', 'Value', '1DReturn', '5DReturn']])
PM_Connection.insertDataFrame(tableDB='IndexesValue', df=Z_DF[['Date', 'Id_RiskFactor', 'Value', '1DReturn', '5DReturn']])
