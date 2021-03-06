import knoema
import pandas as pd

apicfg = knoema.ApiConfig()

data_frame = knoema.get('JODIOIL2018', timerange='2019M4-2020M3', frequency='M', Country='CD;CG;RW;GH;DZ;ZA;LY;EG;GN;LS;AO;CF;SO;BF;GA;TG;SL;LR;DJ;ER;KE;GM;KM;CV;CI;CM;ET;BI;ML;TD;BJ;SZ;GQ;ZW;SD;MW;MZ;NE;GW;TZ;SN;UG;ZM;SS;MG;MU;SC;TN;BW;NG;MA;ST;MR;NA;KZ;JP;MN;PK;AM;BD;LK;AF;BT;TJ;IN;TM;GE;KG;UZ;AZ;KP;MV;KR;NP;CN;AG;BB;DM;GD;KN;LC;VC;CU;GT;DO;JM;CR;PA;HN;NI;BZ;SV;TT;BS;HT;PR;AD;CH;FR;LU;MC;MT;SM;BY;IT;ES;NL;PL;BE;BG;HU;SE;CZ;DK;PT;RO;AT;GR;SK;EE;IE;LT;LV;NO;RU;HR;UA;MD;MK;AL;ME;BA;RS;IS;FI;GB;SI;LI;DE;CA;MX;US;FM;KI;MH;NR;PW;TO;TV;VU;WS;AU;NZ;PG;SB;FJ;HK;MO;TW;PH;MY;TH;SG;VN;LA;MM;TL;BN;KH;ID;VE;BR;AR;CL;CO;PE;EC;PY;UY;BO;GY;SR;CY;TR;BH;YE;KW;OM;QA;IQ;IR;AE;IL;SY;JO;LB;PS;SA', Flow='P.INDPROD', Product='CRUDEOIL', Measure='KBD')

data_frame = knoema.knoema.get()