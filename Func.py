# -*- coding: utf-8 -*-
"""
"""
import numpy as np
import pandas as pd

from datetime import datetime, timedelta
import scipy.stats as st 
import scipy
from scipy.stats import norm
from scipy.optimize import brentq
from scipy.interpolate import interp1d

def ImpliedVolaObjective(S, K, R, D, OPprice,T1,sty):
    B=0
    dcalend=252
    days=T1/dcalend
    D1=(np.log(S/K)+((R-B+((D**2)/2))*days))/(D*(days**0.5))
    D2=((np.log(S/K)+((R-B+((D**2)/2))*days))/(D*(days**0.5)))-D*(days**0.5)
    if "C" in sty:
        return(OPprice - (S*st.norm.cdf(D1)-K*np.exp(-R*days)*st.norm.cdf(D2)))
    else:
        return(OPprice - (K*np.exp(-R*days)*st.norm.cdf(-D2)-S*st.norm.cdf(-D1)))

    
def ImpliedVola(S, K, R, D, OPprice,T1,sty, a=-8.0, b=8.0, xtol=1e-6):
    _S, _K, _R, _T1, _OPprice = S, K, R, T1, OPprice
    def fcn(D):
	    # returns the difference between market and model price at given volatility
        return ImpliedVolaObjective(_S, _K, _R, D, _OPprice, _T1,sty)
   # first we try to return the results from the brentq algorithm
    try:
        result = brentq(fcn, a=a, b=b, xtol=xtol)
        # if the results are *too* small, sent to np.nan so we can later interpolate
        return result
        # return np.nan if result <= xtol else result
    # if it fails then we return np.nan so we can later interpolate the results
    except ValueError:
        return np.nan


def OpitionsPrice(S, K, R, D,T):
    dcalend=252
    days=T/dcalend
    B=0
    D1=(np.log(S/K)+((R-B+((D**2)/2))*days))/(D*(days**0.5))
    D2=((np.log(S/K)+((R-B+((D**2)/2))*days))/(D*(days**0.5)))-D*(days**0.5)

    ValorC=S*st.norm.cdf(D1)-K*np.exp(-R*days)*st.norm.cdf(D2)
    DeltaC=st.norm.cdf(D1)
    GammaC=st.norm.pdf(D1)/(S*D*np.sqrt(days))
    VegaC=S*st.norm.pdf(D1)*(np.sqrt(days))
    ThetaC=(-((S*st.norm.pdf(D1)*D)/(2*np.sqrt(days)))-(R*K*np.exp(-R*days))*st.norm.cdf(D2))/dcalend #252
    RhoC=K*days*np.exp(-R*days)*st.norm.cdf(D2)
    EtasC=DeltaC*S/ValorC

    ValorP=K*np.exp(-R*days)*st.norm.cdf(-D2)-S*st.norm.cdf(-D1)
    DeltaP=-st.norm.cdf(-D1)
    GammaP=st.norm.pdf(D1)/(S*D*np.sqrt(days))
    VegaP=S*st.norm.pdf(D1)*(np.sqrt(days))
    ThetaP=(-((S*st.norm.pdf(D1)*D)/(2*np.sqrt(days)))+(R*K*np.exp(-R*days))*st.norm.cdf(-D2))/dcalend #252
    RhoP=-K*days*np.exp(-R*days)*st.norm.cdf(-D2)
    EtasP=DeltaP*S/ValorP
    return pd.DataFrame({"ValorC":ValorC,
            "DeltaC":DeltaC,
            "GammaC": GammaC,
            "VegaC":VegaC,
            "ThetaC":ThetaC,
            "RhoC": RhoC,
            "EtasC": EtasC,
            "ValorP":ValorP,
            "DeltaP":DeltaP,
            "GammaP": GammaP,
            "VegaP":VegaP,
            "ThetaP":ThetaP,
            "RhoP": RhoP,
            "EtasP": EtasP})
    
def OpitionsPriceImplied(base,x):
    S=base["CLOSE"+str("" if (x-1)==0 else (x-1))+"_ATIVO"].values
    K=base["STRIKE_PRC"].values
    R=base["FreeRiskCLOSE"+str("" if (x-1)==0 else ("_"+(str(x-1))))].values/100
    D=base["BLAKvolat"+str(x)].values
    dcalend=252
    days=base["dayTOexp"].values/dcalend
    B=0
    D1=(np.log(S/K)+((R-B+((D**2)/2))*days))/(D*(days**0.5))
    D2=((np.log(S/K)+((R-B+((D**2)/2))*days))/(D*(days**0.5)))-D*(days**0.5)
    ValorC=S*st.norm.cdf(D1)-K*np.exp(-R*days)*st.norm.cdf(D2)
    DeltaC=st.norm.cdf(D1)
    GammaC=st.norm.pdf(D1)/(S*D*np.sqrt(days))
    VegaC=S*st.norm.pdf(D1)*(np.sqrt(days))
    ThetaC=(-((S*st.norm.pdf(D1)*D)/(2*np.sqrt(days)))-(R*K*np.exp(-R*days))*st.norm.cdf(D2))/dcalend #252
    RhoC=K*days*np.exp(-R*days)*st.norm.cdf(D2)
    EtasC=DeltaC*S/ValorC

    ValorP=K*np.exp(-R*days)*st.norm.cdf(-D2)-S*st.norm.cdf(-D1)
    DeltaP=-st.norm.cdf(-D1)
    GammaP=st.norm.pdf(D1)/(S*D*np.sqrt(days))
    VegaP=S*st.norm.pdf(D1)*(np.sqrt(days))
    ThetaP=(-((S*st.norm.pdf(D1)*D)/(2*np.sqrt(days)))+(R*K*np.exp(-R*days))*st.norm.cdf(-D2))/dcalend #252
    RhoP=-K*days*np.exp(-R*days)*st.norm.cdf(-D2)
    EtasP=DeltaP*S/ValorP
    return pd.DataFrame({"ValorC":ValorC,
            "DeltaC":DeltaC,
            "GammaC": GammaC,
            "VegaC":VegaC,
            "ThetaC":ThetaC,
            "RhoC": RhoC,
            "EtasC": EtasC,
            "ValorP":ValorP,
            "DeltaP":DeltaP,
            "GammaP": GammaP,
            "VegaP":VegaP,
            "ThetaP":ThetaP,
            "RhoP": RhoP,
            "EtasP": EtasP})


def DeltaStreikFilter(optionsInfo_C,lldate,numOpc):
    tempRes=[]
    for exp in lldate:
        temps=optionsInfo_C[(optionsInfo_C.EXPIR_DATE.astype('datetime64')==exp)]
        temps=temps.reindex(temps.Delta.abs().sort_values().index)[:int(numOpc)]
        temps=temps.reindex(temps.STRIKE_PRC.abs().sort_values().index)
        temps=temps.sort_values("STRIKE_PRC")
        temps.index=range(len(temps))
        temps=temps['Instrument'].values
        tempRes=tempRes+[(list(temps))]
    return(list((tempRes)))
