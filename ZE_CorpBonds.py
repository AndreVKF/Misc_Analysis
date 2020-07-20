from API_BBG import BBG_POST
import pandas as pd

########## Italy ##########
ItalyBBG = ['AM017989 Corp','AM133769 Corp','AN613063 Corp','AO149596 Corp','AP443267 Corp','AQ405263 Corp','AW573460 Corp','AX215440 Corp','AX644490 Corp','BG039168 Corp','EC817487 Corp','ED489316 Corp','EI137104 Corp','EI319358 Corp','EJ415238 Corp','EJ810150 Corp','EJ896023 Corp','EJ959750 Corp','EK238202 Corp','EK460904 Corp','EK480568 Corp','EK693447 Corp','EK779082 Corp','EK807683 Corp','EK818925 Corp','JV468065 Corp','JV594814 Corp','LW155835 Corp','LW283691 Corp','QZ661541 Corp','ZP353961 Corp','ZQ094539 Corp','ZR633952 Corp','ZS106935 Corp']

Italy_Bonds = BBG_POST('BDP', ItalyBBG, 'AMT_OUTSTANDING')
Italy_Bonds.reset_index(inplace=True)
Italy_Bonds.rename(columns={'index': 'Ticker'}, inplace=True)


Italy_Bonds_ZSpread = BBG_POST('BDH', ItalyBBG, 'Z_SPRD_MID', date_start=20190101, date_end=20200310)
Italy_Bonds_ZSpread = Italy_Bonds_ZSpread.merge(Italy_Bonds, how='left', on='Ticker')

Italy_Bonds_ZSpread['Base'] = (1 + Italy_Bonds_ZSpread['Z_SPRD_MID']) * Italy_Bonds_ZSpread['AMT_OUTSTANDING']

Italy = Italy_Bonds_ZSpread.dropna()

Italy.groupby('Refdate').apply(lambda x: pd.Series([sum(x.Base)/sum(x.AMT_OUTSTANDING)])).to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\ItalyBonds_Z.csv')

########## Spain ##########
SpainBBG = ['AN216266 Corp','AN216270 Corp','AN763204 Corp','AP306580 Corp','AQ234625 Corp','AR547092 Corp','AR738766 Corp','AR738776 Corp','AR738797 Corp','AU573105 Corp','AX121571 Corp','AX520482 Corp','AX751637 Corp','EK143492 Corp','EK461618 Corp','EK588292 Corp','EK803079 Corp','EK814844 Corp','JK718671 Corp','QZ498658 Corp','ZP389518 Corp','ZQ412374 Corp','ZQ412375 Corp']

Spain_Bonds = BBG_POST('BDP', SpainBBG, 'AMT_OUTSTANDING')
Spain_Bonds.reset_index(inplace=True)
Spain_Bonds.rename(columns={'index': 'Ticker'}, inplace=True)

Spain_Bonds_ZSpread = BBG_POST('BDH',SpainBBG, 'Z_SPRD_MID', date_start=20190101, date_end=20200310)
Spain_Bonds_ZSpread = Spain_Bonds_ZSpread.merge(Spain_Bonds, how='left', on='Ticker')

Spain_Bonds_ZSpread['Base'] = (1 + Spain_Bonds_ZSpread['Z_SPRD_MID']) * Spain_Bonds_ZSpread['AMT_OUTSTANDING']

Spain = Spain_Bonds_ZSpread.dropna()

Spain.groupby('Refdate').apply(lambda x: pd.Series([sum(x.Base)/sum(x.AMT_OUTSTANDING)])).to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\SpainBonds_Z.csv')

pd.pivot_table(Spain, values=['Z_SPRD_MID'], index='Refdate', columns=['Ticker']).to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\SpainBonds.csv')

########## France ##########
FranceBBG = ['AQ286676 Corp','AQ804746 Corp','AT621876 Corp','AT621983 Corp','AU669900 Corp','AW852557 Corp','AZ187081 Corp','EH973309 Corp','EI400413 Corp','EJ516233 Corp','EJ699138 Corp','EJ891119 Corp','EK024568 Corp','EK089367 Corp','EK124413 Corp','EK144722 Corp','EK160676 Corp','EK261914 Corp','EK612958 Corp','EK686365 Corp','EK946829 Corp','JK609904 Corp','QZ515948 Corp','ZR594518 Corp','ZR594522 Corp','ZS215020 Corp']

France_Bonds = BBG_POST('BDP', FranceBBG, 'AMT_OUTSTANDING')
France_Bonds.reset_index(inplace=True)
France_Bonds.rename(columns={'index': 'Ticker'}, inplace=True)

France_Bonds_ZSpread = BBG_POST('BDH',FranceBBG, 'Z_SPRD_MID', date_start=20190101, date_end=20200310)
France_Bonds_ZSpread = France_Bonds_ZSpread.merge(France_Bonds, how='left', on='Ticker')

France_Bonds_ZSpread['Base'] = (1 + France_Bonds_ZSpread['Z_SPRD_MID']) * France_Bonds_ZSpread['AMT_OUTSTANDING']

France = France_Bonds_ZSpread.dropna()

France.groupby('Refdate').apply(lambda x: pd.Series([sum(x.Base)/sum(x.AMT_OUTSTANDING)])).to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\FranceBonds_Z.csv')


pd.pivot_table(France, values=['Z_SPRD_MID'], index='Refdate', columns=['Ticker']).to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\FranceBonds.csv')

################### Italy by Sector ###################

ItalyBBG_Sec = ['AP760894 Corp','ZQ121680 Corp','AU573714 Corp','AS343260 Corp','QZ415620 Corp','AN057650 Corp','ZS053370 Corp','AR813231 Corp','ZR990049 Corp','AU498756 Corp','AP513321 Corp','QZ979675 Corp','EJ349686 Corp','EI183044 Corp','AU573735 Corp','AV577152 Corp','ZQ121679 Corp','AR812812 Corp','AS343403 Corp']

Italy_Bonds = BBG_POST('BDP', ItalyBBG_Sec, ['AMT_OUTSTANDING', 'INDUSTRY_SECTOR'])
Italy_Bonds.reset_index(inplace=True)
Italy_Bonds.rename(columns={'index': 'Ticker'}, inplace=True)


Italy_Bonds_ZSpread = BBG_POST('BDH', ItalyBBG_Sec, 'Z_SPRD_MID', date_start=20190910, date_end=20200310)
Italy_Bonds_ZSpread = Italy_Bonds_ZSpread.merge(Italy_Bonds, how='left', on='Ticker')

Italy_Bonds_ZSpread['Base'] = (1 + Italy_Bonds_ZSpread['Z_SPRD_MID']) * Italy_Bonds_ZSpread['AMT_OUTSTANDING']

Italy = Italy_Bonds_ZSpread.dropna()

SecTest = Italy.groupby(['Refdate', 'INDUSTRY_SECTOR']).apply(lambda x: pd.Series([sum(x.Base)/sum(x.AMT_OUTSTANDING)]))
SecTest.reset_index(inplace=True)
SecTest.rename(columns={0: 'Z_Spread'}, inplace=True)
pd.pivot_table(SecTest, values=['Z_Spread'], index='Refdate', columns='INDUSTRY_SECTOR').to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\ItalySector.csv')


Italy.groupby(['Refdate', 'INDUSTRY_SECTOR']).apply(lambda x: pd.Series([sum(x.Base)/sum(x.AMT_OUTSTANDING)])).to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\ItalyBondsSector_Z.csv')

pd.pivot_table(Italy, values=['Z_SPRD_MID'], index='Refdate', columns=['INDUSTRY_SECTOR']).to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\ItalyBondsSector.csv')











Italy.to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\Italy.csv')

pd.pivot_table(Italy, values=['Z_SPRD_MID'], index='Refdate', columns=['Ticker']).to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\ItalyBonds.csv')


pd.pivot_table(France, values=['Z_SPRD_MID'], index='Refdate', columns=['Ticker']).to_csv('C:\\Users\\andre\\Documents\\Python\\Analysis\\FranceBonds.csv')