#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les Warren @author: warre112
Created on Fri Mar 20 11:58:04 2020
Tutorial Lab08

This program is designed and follows the tutorial "Time Series Analysis with Pandas"
http://earthpy.org/pandas-basics.html
"""
#Import modules needed 
import pandas as pd
import numpy as np
from pandas import Series, DataFrame, Panel
pd.set_option('display.max_rows',15) #limits number of rows displayed 

#Import data from online source 
!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii 


ao = np.loadtxt('monthly.ao.index.b50.current.ascii') #loads data 
ao[0:2]
ao.shape #displays number of rows and columns


#Time Series 
dates = pd.date_range('1950-01', periods=ao.shape[0], freq='M') #creates range
dates
dates.shape

#First Time Series 
AO = Series(ao[:,2], index = dates)
AO
AO.plot() #graph
AO['1980':'1990'].plot()
AO['1980-05':'1981-03'].plot()

AO[120] #individual value 
AO['1960-01'] #by index
AO['1960'] #by specified year
AO[AO > 0] #subset of values


#Data Frame 

#Download dataset (same procedure as begining of tutorial)
!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii
nao = np.loadtxt('norm.nao.monthly.b5001.current.ascii')
dates_nao = pd.date_range('1950-01', periods=nao.shape[0], freq='M')
NAO = Series(nao[:,2], index=dates_nao)
NAO.index

aonao = DataFrame({'AO' : AO, 'NAO' : NAO}) #create data frame 
aonao.plot(subplots=True)
aonao.head()
aonao['NAO']
aonao['Diff'] = aonao['AO'] - aonao['NAO'] #dd new column
aonao.tail()
del aonao['Diff'] #delete column

import datetime
aonao.loc[(aonao.AO >0) & (aonao.NAO <0)
    & (aonao.index > datetime.datetime(1980,1,1))
    & (aonao.index < datetime.datetime(1989,1,1)),
    'NAO'].plot(kind='barh')

#Statistics
aonao.mean()
aonao.max()
aonao.min()
aonao.mean(1) #row-wise mean
aonao.describe() #summary statistics

#Reampling
AO_mm = AO.resample("A").mean() #resampling to a different time frequency, "A" =Annual
AO_mm.plot(style='g--')
AO_mm = AO.resample("A").median()
AO_mm.plot()
AO_mm = AO.resample("3A").apply(np.max)
AO_mm.plot()

AO_mm = AO.resample("A").apply(['mean', np.min, np.max])
AO_mm['1900':'2020'].plot(subplots=True)
AO_mm['1900':'2020'].plot()

#Movign Statistics
aonao.rolling(window=12, center=False).mean().plot(style='-g') #rolling mean
aonao.AO.rolling(window=120).corr(other=aonao.NAO).plot(style='-g') #rolling correlation
aonao.corr() #correlation coefficients 