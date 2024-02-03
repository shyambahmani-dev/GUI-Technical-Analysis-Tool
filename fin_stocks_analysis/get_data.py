import numpy as np
import pandas as pd
import matplotlib as mpl
import yfinance as yf
import datetime
import csv
import os
import code
import time
from dateutil.relativedelta import relativedelta
from pandas import ExcelWriter
import inline
import traceback
import warnings
warnings.filterwarnings("ignore")


"""

try:
    
    data1name = str("^NSEI") #tickername
    ticker1name = data1name
    ticker1 = yf.Ticker(ticker1name)
    startdate = datetime.date.today() - relativedelta(days = 7) - relativedelta(years = 15)
    enddate = datetime.date.today() + relativedelta(days = 1)

    #startdate = datetime.date(2018, 12, 29)
    #enddate = datetime.date(2021 , 1, 7)

except Exception as exp:
    
    print(exp)
    input()

#"""



#### -- Get OHLC -- ####


def tickerData(symbol, periodTested = '0', intervalTested = '1d', startdate = datetime.date.today() - relativedelta(days = 57), enddate = datetime.date.today(), from_dates = False):

    try:

        #print("\n\n\n\nThe Stock in analysis is %s\n\n\n\n" %(symbol))


        ticker1 = yf.Ticker(symbol)

        #startdate = datetime.date.today() - relativedelta(days = 7) - relativedelta(years = 15)
        #enddate = datetime.date.today() + relativedelta(days = 1)



        if( from_dates == False ):

            if(periodTested == '0'):

                if intervalTested in ('1m', '2m,' '5m', '15m', '30m', '1h'):
                    
                    if intervalTested == '1m':
                        days = 7 
                    elif intervalTested == '1h':
                        days = 718
                    else:
                        days = 57
                    
                    start_date = datetime.datetime.now()-datetime.timedelta(days=days)

                    if( os.path.isfile( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ) ) ):
                        data1 = pd.read_csv( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ), index_col = [0] )
                        data1.index = pd.to_datetime(data1.index)
                    else:
                        data1 = pd.DataFrame( ticker1.history( interval = intervalTested, start= start_date, end= datetime.datetime.today() ) )
                        data1.to_csv( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ) )

                else:
                    
                    periodTested = 'max'
                    
                    if( os.path.isfile( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ) ) ):
                        data1 = pd.read_csv( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ), index_col = [0] )
                        data1.index = pd.to_datetime(data1.index)
                    else:
                        data1 = pd.DataFrame( ticker1.history( period = periodTested , interval = intervalTested ) )
                        data1.to_csv( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ) )
                
            else:

                if intervalTested in ('1m', '2m,' '5m', '15m', '30m', '1h'):
                    
                    if intervalTested == '1m':
                        days = 7
                    elif intervalTested == '1h':
                        days = 720
                    else:
                        days = 57
                    
                    start_date = datetime.datetime.now()-datetime.timedelta(days=days)
                        
                    if( os.path.isfile( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ) ) ):
                        data1 = pd.read_csv( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ), index_col = [0] )
                        data1.index = pd.to_datetime(data1.index)
                    else:
                        data1 = pd.DataFrame( ticker1.history( interval = intervalTested, start= start_date, end= datetime.datetime.today() ) )
                        data1.to_csv( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ) )
                        
                else:

                    if( os.path.isfile( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ) ) ):
                        data1 = pd.read_csv( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ), index_col = [0] )
                        data1.index = pd.to_datetime(data1.index)
                    else:
                        data1 = pd.DataFrame( ticker1.history( period = periodTested , interval = intervalTested ) )
                        data1.to_csv( r".\database\%s-%s-%s-%s.csv" %(symbol, periodTested, (str)(datetime.datetime.today().date()), intervalTested ) )


            data1 = data1.astype(dtype={'Open':float, 'High':float, 'Low':float, 'Close':float, 'Volume':float})
            
            data1kindex = data1.index.values
            tempDate = np.array([])
            for i in data1kindex:
                i = pd.to_datetime(i)
                tempDate = np.append(tempDate,i)
            data1.index = tempDate
            
            #print("Dataset of %f values from %s to %s: \n%s\n\n\n" %(data1.size, startdate , enddate , data1) )
            
        elif(from_dates == True):

            if( os.path.isfile( r".\database\%s-%s-%s-%s.csv" %(symbol, startdate, enddate, intervalTested ) ) ):
                data1 = pd.read_csv( r".\database\%s-%s-%s-%s.csv" %(symbol, startdate, enddate, intervalTested ), index_col = [0] )
                data1.index = pd.to_datetime(data1.index)

            
            else:
            
                strat_days = enddate - startdate
                strat_days = strat_days.days
                print("strat_days = %s" %(strat_days) )

                
                if intervalTested in ('1m', '2m,' '5m', '15m', '30m', '1h'):
                    
                    if( intervalTested == '1m'):
                        if(strat_days > 7 ):
                            days = 7
                            startdate = enddate-datetime.timedelta(days=days)
                    elif( intervalTested == '1h'):
                        if(strat_days > 718):
                            days = 718
                            startdate = enddate-datetime.timedelta(days=days)
                    else:
                        if(strat_days > 57):
                            days = 57
                            startdate = enddate-datetime.timedelta(days=days)
                
                
                data1 = pd.DataFrame( ticker1.history( interval = intervalTested, start= startdate, end= enddate ) )
                data1.to_csv( r".\database\%s-%s-%s-%s.csv" %(symbol, startdate, enddate, intervalTested ) )


        if(data1.size == 0):
            print("Error fetching data, please check if symbol exists")

        return data1


    except Exception as exp:
        
        print(exp)
        input()




################################3





def tickerDataLive(symbol, periodTested = '0', intervalTested = '1d', startdate = datetime.date.today() - relativedelta(days = 57), enddate = datetime.date.today()):

    try:

        #print("\n\n\n\nThe Stock in analysis is %s\n\n\n\n" %(symbol))


        ticker1 = yf.Ticker(symbol)

        #startdate = datetime.date.today() - relativedelta(days = 7) - relativedelta(years = 15)
        #enddate = datetime.date.today() + relativedelta(days = 1)





        if(periodTested == '0'):

            if intervalTested in ('1m', '2m,' '5m', '15m', '30m', '1h'):
                
                if intervalTested == '1m':
                    days = 7 
                elif intervalTested == '1h':
                    days = 250
                else:
                    days = 55
                
                start_date = datetime.datetime.now()-datetime.timedelta(days=days)

                data1 = pd.DataFrame( ticker1.history( period= periodTested, interval = intervalTested, start= start_date, end= datetime.datetime.today() ) )

            else:
                
                periodTested = '1d'
                
                data1 = pd.DataFrame( ticker1.history( period= periodTested , interval= intervalTested ) )
            
        else:

            if intervalTested in ('1m', '2m,' '5m', '15m', '30m', '1h'):
                
                if intervalTested == '1m':
                    days = 7 
                elif intervalTested == '1h':
                    days = 718
                else:
                    days = 58
                
                start_date = datetime.datetime.now()-datetime.timedelta(days=days)
                    
                data1 = pd.DataFrame( ticker1.history( period= periodTested, interval= intervalTested, start= start_date, end= datetime.datetime.today() ) )
            
            else:

                data1 = pd.DataFrame( ticker1.history( interval= intervalTested, period= periodTested ) )


        data1 = data1.astype(dtype={'Open':float, 'High':float, 'Low':float, 'Close':float, 'Volume':float})
        
        data1kindex = data1.index.values
        tempDate = np.array([])
        for i in data1kindex:
            i = pd.to_datetime(i)
            tempDate = np.append(tempDate,i)
        data1.index = tempDate
        

        if(data1.size == 0):
            print("Error fetching data, please check if symbol exists")

        return data1


    except Exception as exp:
        
        print(exp)
        input()


#### -- Get OHLC -- ####
















def tickerDataDeployed(symbol, intervalTested = '1d'):

    try:

        ticker1 = yf.Ticker(symbol)


        if( os.path.isfile( r".\database\%s-%s-deployed.csv" %(symbol, intervalTested) ) ):
            data1 = pd.read_csv( r".\database\%s-%s-deployed.csv" %(symbol, intervalTested), index_col = [0] )
            data1.index = pd.to_datetime(data1.index, utc= True)
        else:
            data1 = tickerDataLive(symbol = symbol, intervalTested = intervalTested)
            data1.to_csv( r".\database\%s-%s-deployed.csv" %(symbol, intervalTested) )
    
        return data1

    except Exception as exp:
        
        print(exp)
        input()



def portfolioDeployed(symbol, intervalTested = '1d'):

    try:

        ticker1 = yf.Ticker(symbol)

        if( os.path.isfile( r".\database\portfolio-%s-%s.csv" %(symbol, intervalTested) ) ):
            data1 = pd.read_csv( r".\database\portfolio-%s-%s.csv" %(symbol, intervalTested), index_col = [0] )
            data1.index = pd.to_datetime(data1.index)
        else:
            data1 = pd.DataFrame(columns=['Value','AssetNum','Cash'])
            data1.to_csv( r".\database\%s-%s-deployed.csv" %(symbol, intervalTested) )
    
        return data1

    except Exception as exp:
        
        print(exp)
        input()
