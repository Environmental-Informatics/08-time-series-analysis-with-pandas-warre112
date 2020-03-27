#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les Warren @author: warre112
Created on Mon Mar 16 11:56:45 2020
Lab08- Time Series with Panda

This program is designed to read input file, perform time series analysis, and export outputs as pdf files 
"""

import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series
pd.set_option('display.max_rows',15) #limit number of printed rows

#Input data using read_table
Data = pd.read_table('WabashRiver_DailyDischarge_20150317-20160324.txt', header = 13, 
                       skiprows=11, usecols=[2,3,4], names=['DateTime','TZ','Discharge(cfs)'], parse_dates=[[0,1]]) 

Data = Data.drop(0) #eliminating non-numeric row 
Data['Discharge(cfs)']= pd.to_numeric(Data['Discharge(cfs)'])
# time series
dates = pd.date_range('2015-03-17 00:00', periods=Data.shape[0], freq='15min') #date range, 15 minute intervals 
data2 = Series(Data['Discharge(cfs)'].values, index=dates) 


data_rs = data2.resample("D").mean() #reample to get daily mean 


ax= data2.plot() #plot figure 
ax.set_ylabel('Mean Daily Discharge (cfs)')
ax.set_xlabel('Month')
plt.savefig('Daily_Streamflow.pdf')

#Highest Daily stream flow
HF = data_rs.nlargest(10) #ten days with highest average streamflow

data_rs.plot(color='blue', alpha=0) #set axis like first figure 
plt.scatter(HF.index,HF.values,s=20,c='black',marker='x')
plt.ylabel('Mean Daily Discharge (cfs)')
plt.xlabel('Month')
plt.savefig('Ten_Highest.pdf')

#Reample for Monthly Average Flow
Month = data2.resample("M").mean()

Month.plot()
plt.ylabel('Mean Monthly Discharge (cfs)')
plt.xlabel('Month')
plt.savefig('Monthly_Streamflow.pdf')
