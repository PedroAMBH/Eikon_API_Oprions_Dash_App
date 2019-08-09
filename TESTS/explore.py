# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 20:07:59 2019

@author: pedro
"""

import eikon as ek
import numpy as np
import pandas as pd
import json 
from business_duration import businessDuration
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.offline import plot
import time
import Func
from plotly.subplots import make_subplots
import scipy.interpolate



def update_output(n_clicks, value):
    lista, err = ek.get_data(value,'RData')
    lista=lista.Instrument[~lista.Instrument.isnull()].values
    optionsInfo, err = ek.get_data(list(lista),['TRADE_DATE','TRDPRC_1',"PUTCALLIND","EXPIR_DATE","STRIKE_PRC","BKGD_REF"])
    optionsInfo=optionsInfo[optionsInfo.STRIKE_PRC.notnull()]
    #spot, err = ek.get_data(optionsInfo.BKGD_REF.values[0],['TRADE_DATE','TRDPRC_1',"PUTCALLIND","EXPIR_DATE","STRIKE_PRC","BKGD_REF"])
    spot, err = ek.get_data([optionsInfo.BKGD_REF.values[0]]+['BRSELICD=CBBR'],['TRADE_DATE','TRDPRC_1'])
    optionsInfo['Delta']=spot.TRDPRC_1.values[0]-optionsInfo.STRIKE_PRC
    optionsInfo_C=optionsInfo[optionsInfo.PUTCALLIND=='CALL']
    optionsInfo_P=optionsInfo[optionsInfo.PUTCALLIND!='CALL']

    return (optionsInfo_C,optionsInfo_P,list(set(optionsInfo.EXPIR_DATE.values)))

def DeltaStreikFilter(optionsInfo_C,lldate,numOpc):
    tempRes=[]
    for exp in lldate:
        temps=optionsInfo_C[(optionsInfo_C.EXPIR_DATE.astype('datetime64')==exp)]
        temps=temps.reindex(temps.Delta.abs().sort_values().index)[:numOpc]
#        temps=temps.sort_values("STRIKE_PRC")
#        temps=temps.reindex(temps.STRIKE_PRC.abs().sort_values().index)
#        temps=temps.reindex(temps.Instrument.sort_values().index)
#        temps=temps.sort_values("Instrument")
#        temps.index=range(len(temps))
        temps=temps['Instrument'].values
        tempRes=tempRes+[(list(temps))]
    return(list((tempRes)))

 
value='b62c1ab67f2d457980440a42dbe099dd868d6a29'
ek.set_app_key(value)

value='0#PETR4*.SA'
lista, err = ek.get_data(value,'RData')
lista=lista.Instrument[~lista.Instrument.isnull()].values

optionsInfo, err = ek.get_data(list(lista),['TRADE_DATE','TRDPRC_1',"PUTCALLIND","EXPIR_DATE","STRIKE_PRC","BKGD_REF"])
optionsInfo=optionsInfo[optionsInfo.STRIKE_PRC.notnull()]
optionsInfo=optionsInfo[optionsInfo.EXPIR_DATE.astype('datetime64')>optionsInfo.TRADE_DATE.astype('datetime64').max()]

#spot, err = ek.get_data(optionsInfo.BKGD_REF.values[0],['TRADE_DATE','TRDPRC_1',"PUTCALLIND","EXPIR_DATE","STRIKE_PRC","BKGD_REF"])
spot, err = ek.get_data([optionsInfo.BKGD_REF.values[0]]+['BRSELICD=CBBR'],['TRADE_DATE','TRDPRC_1'])
optionsInfo['Delta']=spot.TRDPRC_1.values[0]-optionsInfo.STRIKE_PRC
optionsInfo_C=optionsInfo[optionsInfo.PUTCALLIND=='CALL']
optionsInfo_P=optionsInfo[optionsInfo.PUTCALLIND!='CALL']


lldate=list(set(optionsInfo.EXPIR_DATE.values))
lldate.sort()
lldate=lldate[:3]

numOpc=21

Selec_C=DeltaStreikFilter(optionsInfo_C,lldate,numOpc)
Selec_P=DeltaStreikFilter(optionsInfo_P,lldate,numOpc)

callRIC=pd.DataFrame(Selec_C).T
callRIC.columns=lldate
call=pd.DataFrame([optionsInfo[optionsInfo.Instrument.isin(Selec_C[i])].STRIKE_PRC.values for i in range(len(Selec_C))]).T
call.columns=lldate

putRIC=pd.DataFrame(Selec_P).T
putRIC.columns=lldate
put=pd.DataFrame([optionsInfo[optionsInfo.Instrument.isin(Selec_P[i])].STRIKE_PRC.values for i in range(len(Selec_P))]).T
put.columns=lldate

putRIC.append(callRIC)


data=optionsInfo[optionsInfo.STRIKE_PRC.notnull()&optionsInfo.TRADE_DATE.notnull()].sample(n=3)

putRIC.values[:,1]
callRIC.values[:,1]

lll=['PETR4U270.SA', 'PETR4I270.SA']
data=optionsInfo[optionsInfo.Instrument.isin(lll)]
data['Amount']=[-1000,-1000]
#data['Amount']=np.random.randint(-1,1, size=len(data))

data['Amount']=data['Amount'].astype(float)
data['TRDPRC_1']=data['TRDPRC_1'].astype(float)
data['STRIKE_PRC']=data['STRIKE_PRC'].astype(float)
data["TRADE_DATE"]=pd.to_datetime(data["TRADE_DATE"])
data["EXPIR_DATE"]=pd.to_datetime(data["EXPIR_DATE"])

#data['PUTCALLIND']=['CALL','CALL']


ssp=spot[spot["Instrument"]!="BRSELICD=CBBR"].TRDPRC_1.values[0]

days=(data.apply(lambda row: businessDuration(startdate=row['TRADE_DATE'],enddate=row['EXPIR_DATE'],unit='day'), axis=1)).values

j=0
ImpyVola=[round(Func.ImpliedVola(spot[spot["Instrument"]!="BRSELICD=CBBR"].TRDPRC_1.values[0].astype(float),
            data["STRIKE_PRC"].values[j].astype(float),
            spot[spot["Instrument"]=="BRSELICD=CBBR"].TRDPRC_1.values[0].astype(float)/100,
            .70,
            data["TRDPRC_1"].values[j].astype(float),
            days[j],
            # (((data["EXPIR_DATE"].values[j])-(data["TRADE_DATE"].values[j])).astype('timedelta64[D]').astype(int)),
            data["PUTCALLIND"],a=-12.0, b=12.0, xtol=1e-8)*100,2) for j in range(len(data))]


GREEKS=Func.OpitionsPrice(spot[spot["Instrument"]!="BRSELICD=CBBR"].TRDPRC_1.values[0].astype(float),
                            data["STRIKE_PRC"].values.astype(float),
                            spot[spot["Instrument"]=="BRSELICD=CBBR"].TRDPRC_1.values[0].astype(float)/100,
                            np.array(ImpyVola)/100,
                            days)


data[['Valor','Delta','Gamma','Vega','Theta','Rho','Etas']]=pd.DataFrame([[0 for i in range(7)]], columns=['Valor','Delta','Gamma','Vega','Theta','Rho','Etas'],index=data.index)

callGreek=GREEKS[list(GREEKS.columns[GREEKS.columns.str.contains('C', regex=True)])][data.PUTCALLIND.str.contains('C', regex=True).values]
putGreek=GREEKS[list(GREEKS.columns[GREEKS.columns.str.contains('P', regex=True)])][data.PUTCALLIND.str.contains('P', regex=True).values]

callGreek.columns=['Valor','Delta','Gamma','Vega','Theta','Rho','Etas']
putGreek.columns=['Valor','Delta','Gamma','Vega','Theta','Rho','Etas']

data.loc[list(data.PUTCALLIND.str.contains('C', regex=True).values),['Valor','Delta','Gamma','Vega','Theta','Rho','Etas']]=callGreek.values
data.loc[list(data.PUTCALLIND.str.contains('P', regex=True).values),['Valor','Delta','Gamma','Vega','Theta','Rho','Etas']]=putGreek.values


vola, err = ek.get_data([spot[spot["Instrument"]!="BRSELICD=CBBR"].Instrument.values[0]],
                            ['TR.Volatility5D','TR.Volatility10D',"TR.Volatility20D",
                            "TR.Volatility30D","TR.Volatility60D","TR.Volatility90D"])

vola.columns=['Instrument',5,10,20,30,60,90]
vola[[5,10,20,30,60,90]]=vola[[5,10,20,30,60,90]]/100
days=list(np.unique(days))

dists=[]
vollist=[]
for d in days:
    y_interp = scipy.interpolate.interp1d(vola.columns[1:].astype(float),vola.T[0].values[1:].astype(float))
    volaV=y_interp(d)
    Distrib=1-np.random.normal(0,(volaV/(252**0.5)*(d**0.5)), size=5000)
    Distrib=Distrib*ssp

    vollist.append(volaV)
    dists.append(Distrib)

Price=dists[pd.DataFrame(dists).max(1).argmax()]
Price.sort()
net=[]
for k in range(len(data)):
    if data['Amount'].iloc[k]>=0:
        if "C" in data['PUTCALLIND'].iloc[k]:
            Rt= -data['STRIKE_PRC'].iloc[k]-data['TRDPRC_1'].iloc[k] +Price
            Rt[Rt<=-data['TRDPRC_1'].iloc[k]]=-data['TRDPRC_1'].iloc[k]
            Rt=Rt*abs(data['Amount'].iloc[k])
            net.append(list(Rt))
        else:
            Rt= data['STRIKE_PRC'].iloc[k] -data['TRDPRC_1'].iloc[k] -Price
            Rt[Rt<=-data['TRDPRC_1'].iloc[k]]=-data['TRDPRC_1'].iloc[k]
            Rt=Rt*abs(data['Amount'].iloc[k])
            net.append(list(Rt))

    else:
        if "C" in data['PUTCALLIND'].iloc[k]:
            Rt= data['STRIKE_PRC'].iloc[k] +data['TRDPRC_1'].iloc[k] -Price
            Rt[Rt>=data['TRDPRC_1'].iloc[k]]=data['TRDPRC_1'].iloc[k]
            Rt=Rt*abs(data['Amount'].iloc[k])
            net.append(list(Rt))
        else:
            Rt= -data['STRIKE_PRC'].iloc[k] +data['TRDPRC_1'].iloc[k] +Price
            Rt[Rt>=data['TRDPRC_1'].iloc[k]]=data['TRDPRC_1'].iloc[k]
            Rt=Rt*abs(data['Amount'].iloc[k])
            net.append(list(Rt))

pay=pd.DataFrame(net)
pay.columns=Price
pays=pay
print(pays.values)
pay=pay.sum()

tempTT=[]
for j in range(len(set(days))):
    tempT=[]
    for s in range(len(data["STRIKE_PRC"])):
        temp=Func.OpitionsPrice(Price,
                            data["STRIKE_PRC"].values.astype(float)[s],
                            spot[spot["Instrument"]=="BRSELICD=CBBR"].TRDPRC_1.values[0].astype(float)/100,
                            np.array(ImpyVola[j])/100,
                            days[j])
        
        if "C" in data["PUTCALLIND"].values[s]:
            temp=list((temp.ValorC.values-data['TRDPRC_1'].values[s])*data['Amount'].values[s])
        else:
            temp=list((temp.ValorP.values-data['TRDPRC_1'].values[s])*data['Amount'].values[s])

        tempT.append(temp)

    tempTT.append(tempT)


fig = go.FigureWidget(make_subplots(shared_xaxes=True, specs=[[{"secondary_y": True}]],print_grid=False))
trace3 = go.Scatter(name="0 line",x=pay.index,
                       y=np.array([0 for i in Distrib]),
                       xaxis = 'x1',yaxis = 'y2',
                       line = dict(color='black', width=2, dash='dash'))
fig.add_trace(trace3, secondary_y=False)

trace1 = go.Scatter(name="Payoff",x=pay.index,
                       y=pay.values,xaxis = 'x1',yaxis = 'y2',
                       mode='lines',fill='tozeroy')
fig.add_trace(trace1, secondary_y=False)

for i in range(len(tempTT)):
    trace5 = go.Scatter(name="Price - "+str(days[j]),x=pay.index,
                           y=pd.DataFrame(tempTT[i]).sum().values,
                           xaxis = 'x1',yaxis = 'y2',
                           mode='lines')
    fig.add_trace(trace5, secondary_y=False)


for lin,i in zip(pays.values,pays.index):
    trace4 = go.Scatter(name=data.Instrument.values[i],x=pay.index,
                           y=lin,xaxis = 'x1',yaxis = 'y2',
                           line = dict(width=2, dash='dash'))
    fig.add_trace(trace4, secondary_y=False)


for i,j in zip(days,dists):
    trace2 = ff.create_distplot([j],[str(i)+" Days - Probabilidade"], bin_size=.5,curve_type='normal',show_hist=False,show_rug=False)
    fig.add_trace(trace2['data'][0], secondary_y=True)

prob=round(sum(pay.values>0)/len(Distrib)*100,2)
plot(fig, auto_open=True)

sum(pay>0)/len(Distrib)*100

str(round(sum(pay>0)/len(Distrib)*100,2))+"%"

str(round(sum(pay>0)/len(Distrib)*100,2))+"%"

