import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.widgets as mplw
import yfinance as yf
import datetime
import scipy as sp
import scipy.stats as stats
import math
from matplotlib.backends.backend_pdf import PdfPages, FigureCanvasPdf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import time
import os
from dateutil.relativedelta import relativedelta
from pandas import ExcelWriter
import traceback
import warnings
warnings.filterwarnings("ignore")


import mplfinance as mpf

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

import sys
sys.path.append(".")

import get_data as getData
import get_indicators as getIndicators
from drawer import Drawer
from stats_func import *


print("Statistics and plotting program")


try:

    ticker1name = str("TATAMOTORS.NS")
    ticker1 = yf.Ticker(ticker1name)
    
    #### -- Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo] -- ####
    
    intervalAnalysed = '1d'

    #startdate = datetime.date.today() - relativedelta(days = 7) - relativedelta(years = 10)
    #enddate = datetime.date.today() + relativedelta(days = 1)

    #startdate = datetime.date(2018, 12, 29)



    print("\n\n\n\nThe Stock in analysis is %s\n\n\n\n" %(ticker1name))
    
    data1 = getData.tickerData(ticker1name, intervalTested = intervalAnalysed)

    startdate = data1.index[0]
    enddate = data1.index[-1]

    try:

        if os.path.isdir("D:\Finance\Stocks\Company Data\Recent\%s" %(ticker1name) ) :
            
            pass

        else:

            os.mkdir("D:\Finance\Stocks\Company Data\Recent\%s" %(ticker1name) )


    except:
        
        print(traceback.print_exc())
        input("\nError BC.\n")


    data1.to_csv(r"D:\Finance\Stocks\Company Data\Recent\%s\%s-%s-%s.csv" %( ticker1name , ticker1name , startdate.date() , enddate.date() ) )


    data1size = int(len(data1.index))
    print("Total size of dataset = " , data1size , "\n")
    rangedata1 = range(0 , data1size)

    mnthdates = pd.date_range(startdate,enddate,freq = 'MS')



    start = time.time()


    pd.options.mode.chained_assignment = None
    
    data1RSI = getIndicators.getRSI(data1)
    data1DMA = getIndicators.getDMA(data1)
    data1EMA = getIndicators.getEMA(data1)
    
    data1DMASlope = data1DMA.diff()
    data1EMASlope = data1EMA.diff()
    
    data1RSI = getIndicators.getRSI(data1)
    data1BB = getIndicators.getBB(data1, interval = 14)
    
        
except:
    
    print(traceback.print_exc())
    input("\nError BC.\n")








#### -- Graphing and plotting -- ####



try:

    lastprice = float(data1["Close"].tail(1))
    magoften = 1
    magofdata1 = 1

    while True:
            
        if int(lastprice/magoften) == 0:
            magofdata1 = magoften
            break
        
        else:
        
            magoften = magoften*10
    
    magofdata1 = magofdata1/100
    
    
except:
    
    print(traceback.print_exc())
    input("\nError BC.\n")



## -- OHLC Chart -- ##










## -- OHLC Chart completed -- ##



## -- Plotting and Charting -- ##

colorsForPlot = ["royalblue", "green", "orchid", "gold", "brown", "deepskyblue", "pink", "magenta", "paleblue", "black", "orange", "darkviolet", "slategrey"]


def ohlcplot(data1, ax, fig):
        
    mpf.plot(data1, type='candle', ax= ax, style='yahoo')
    ax.set_ylim( data1["Close"].min() - data1["Close"].mean()/100 , data1["Close"].max() + data1["Close"].mean()/100 )
    


def linesPlot(ax, fig, data1ToPlot, toPlot = [5, 10, 25, 50, 100, 200]):
        
    colInd = 0
    
    for it in toPlot:
        
        ax.plot( range(0, data1ToPlot.index.size) , data1ToPlot["%s" %(it)], label = "%s" %(it), color = colorsForPlot[colInd] , alpha = 0.7)
        colInd += 1
        
    colInd = 0

        

def scatterPlot(ax, fig, data1ToPlot, label, color):

    data1Mean = data1ToPlot.mean()
    data1StD = data1ToPlot.std()

    ax.scatter( range(0, data1ToPlot.index.size) , data1ToPlot, label = label, color = color , marker = "." )
    ax.axhline( data1Mean , color = color )
    ax.axhline( data1Mean + data1StD , color = color )
    ax.axhline( data1Mean - data1StD , color = color )
    ax.axhline( ( int(0) ) , color = "red" , alpha = 0.5 )





try:



    def plotshowkar():
        plt.show()
        pass


    #### -- OHLC Chart -- ####


    fig1 = plt.figure(figsize = (12,12))
    fig1.canvas.manager.set_window_title("OHLC Chart")

    gs1 = fig1.add_gridspec(4,4)
    
    ax101 = fig1.add_subplot(gs1[:,0:3])
    ax101.set_title("%s - OHLC chart from %s to %s " %(ticker1name, startdate.date() , enddate.date()))
    ohlcplot(data1, ax101, fig1)
    plotkarde101 = Drawer(ax101,fig1)
    ax101.legend()
    
    mcursor1 = mplw.MultiCursor(fig1.canvas , [ax101] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig1.tight_layout()

    #### -- E.O. OHLC Chart -- ####





    #### -- Close Price Chart -- ####

    fig1_1 = plt.figure(figsize = (12,12))
    fig1_1.canvas.manager.set_window_title("Close Price Line Chart")

    gs1_1 = fig1_1.add_gridspec(4,4)
    ax1_101 = fig1_1.add_subplot(gs1_1[:,0:3])
    ax1_101.set_title("%s - Close Price chart from %s to %s " %(ticker1name, startdate.date() , enddate.date()))

    ax1_101.plot( data1.index , data1["Close"] , label = "%s Close" %(ticker1name) , color = "grey")
    plotkarde1_101 = Drawer(ax1_101,fig1_1)
    ax1_101.legend()

    mcursor1_1 = mplw.MultiCursor(fig1_1.canvas , [ax1_101] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig1_1.tight_layout()

    #### -- E.O. Close Price Chart -- ####






    #### -- DMA Chart -- ####
    
    fig2 = plt.figure(figsize = (12,12))
    fig2.canvas.manager.set_window_title("DMA Chart")

    gs2 = fig2.add_gridspec(4,4)

    ax201 = fig2.add_subplot(gs2[:,0:3])
    ax201.set_title("%s - DMAs through %s - %s" %(ticker1name, startdate.date(), enddate.date()))
    ohlcplot(data1, ax201, fig2)
    linesPlot(ax201, fig2, data1DMA)
    ax201.legend()
    plotkarde201 = Drawer(ax201,fig2)
    
    mcursor2 = mplw.MultiCursor(fig2.canvas, [ax201] , horizOn= True, color = "lightskyblue" , linewidth = 1)
    fig2.tight_layout()

    #### -- E.O. DMA Chart -- ####
    
    
    



    #### -- Fast DMA 1st and 2nd Differential Chart Fast-- ####

    fig4_1 = plt.figure(figsize = (12,12))
    fig4_1DMA = 10
    fig4_1.canvas.manager.set_window_title("1st and 2nd Differential %sDMA through %s - %s" %(fig4_1DMA, startdate.date(), enddate.date()))
    

    gs4_1 = fig4_1.add_gridspec(5,4)
    
    
    ax4_101 = fig4_1.add_subplot(gs4_1[0:3,0:3])
    ohlcplot(data1, ax4_101, fig4_1)
    linesPlot(ax4_101, fig4_1, data1DMA)
    plotkarde4_102 = Drawer(ax4_101,fig4_1)
    ax4_101.legend()

    
    ax4_102 = fig4_1.add_subplot(gs4_1[3:4,0:3] , sharex = ax4_101)
    ax4_102.set_title("%s - 1st Differential %sDMA through %s - %s" %(ticker1name, fig4_1DMA, startdate.date(), enddate.date()))
    scatterPlot(ax4_102, fig4_1, data1DMASlope["%s" %(fig4_1DMA)], label = "%sDMA Slope" %(fig4_1DMA), color = "blue")
    plotkarde4_102 = Drawer(ax4_102,fig4_1)
    ax4_102.legend()


    ax4_103 = fig4_1.add_subplot(gs4_1[4:5,0:3] , sharex = ax4_101)
    ax4_103.set_title("%s - 2nd Differential (smoothed 3MA) %sDMA through %s - %s" %(ticker1name, fig4_1DMA, startdate.date(), enddate.date()))
    scatterPlot(ax4_103, fig4_1, data1DMASlope["%s" %(fig4_1DMA)].diff().rolling(3).mean(), label = "%sDMA Diff^2" %(fig4_1DMA), color = "slateblue")
    plotkarde4_103 = Drawer(ax4_103,fig4_1)
    ax4_103.legend()
    
    mcursor4_1 = mplw.MultiCursor(fig4_1.canvas, [ax4_101,ax4_102,ax4_103] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig4_1.tight_layout()

    #### -- E.O. Fast DMA 1st and 2nd Differential Chart -- ####



    



    #### -- Slow DMA 1st and 2nd Differential Chart -- ####

    fig4_2 = plt.figure(figsize = (12,12))
    fig4_2DMA = 50
    
    fig4_2.canvas.manager.set_window_title("1st and 2nd Differential %sDMA through %s - %s" %(fig4_2DMA, startdate.date(), enddate.date()))

    gs4_2 = fig4_2.add_gridspec(5,4)
    
    
    ax4_201 = fig4_2.add_subplot(gs4_2[0:3,0:3])
    ohlcplot(data1, ax4_201, fig4_2)
    linesPlot(ax4_201, fig4_2, data1DMA)
    plotkarde4_202 = Drawer(ax4_201,fig4_2)
    ax4_201.legend()

    
    ax4_202 = fig4_2.add_subplot(gs4_2[3:4,0:3] , sharex = ax4_201)
    ax4_202.set_title("%s - 1st Differential %sDMA through %s - %s" %(ticker1name, fig4_2DMA, startdate.date(), enddate.date()))
    scatterPlot(ax4_202, fig4_2, data1DMASlope["%s" %(fig4_2DMA)], label = "%sDMA Slope" %(fig4_2DMA), color = "blue")
    plotkarde4_202 = Drawer(ax4_202,fig4_2)
    ax4_202.legend()


    ax4_203 = fig4_2.add_subplot(gs4_2[4:5,0:3] , sharex = ax4_201)
    ax4_203.set_title("%s - 2nd Differential (smoothed 3MA) %sDMA through %s - %s" %(ticker1name, fig4_2DMA, startdate.date(), enddate.date()))
    scatterPlot(ax4_203, fig4_2, data1DMASlope["%s" %(fig4_2DMA)].diff().rolling(3).mean(), label = "%sDMA Diff^2" %(fig4_2DMA), color = "slateblue")
    plotkarde4_203 = Drawer(ax4_203,fig4_2)
    ax4_203.legend()
    
    mcursor4_2 = mplw.MultiCursor(fig4_2.canvas, [ax4_201,ax4_202,ax4_203] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig4_2.tight_layout()

    #### -- E.O. Slow DMA 1st and 2nd Differential Chart Fast-- ####





    #### -- DMA Difference Chart -- ####

    fig8 = plt.figure(figsize=(12,12))
    fig8DMAFast = 10
    fig8DMASlow = 50
    fig8.canvas.manager.set_window_title("%sDMA-%sDMA through %s - %s" %(fig8DMAFast, fig8DMASlow, startdate.date(), enddate.date()))
        
    gs8 = fig8.add_gridspec(5,4)

    ax801 = fig8.add_subplot(gs8[0:3,0:3])
    ax801.set_title("%s - %sDMA-%sDMA through %s - %s" %(ticker1name, fig8DMAFast, fig8DMASlow, startdate.date(), enddate.date()))
    ohlcplot(data1, ax801, fig8)
    linesPlot(ax801, fig8, data1DMA, [fig8DMAFast, fig8DMASlow])
    plotkarde801 = Drawer(ax801,fig8)
    
    
    ax802 = fig8.add_subplot(gs8[3:5,0:3] , sharex = ax801)
    ax802.axhline( int(0) , color = "red" , alpha = 0.5 )
    ax802.bar( rangedata1 , (data1DMA["%s" %(fig8DMAFast)] - data1DMA["%s" %(fig8DMASlow)]) , color = "blue" , alpha = 0.5 , label = "SMA 10 - 50")
    plotkarde802 = Drawer(ax802,fig8)
    
    mcursor8 = mplw.MultiCursor(fig8.canvas, [ax801,ax802] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig8.tight_layout()

    #### -- E.O. DMA Difference Chart -- ####




    






    #### -- EMA Chart -- ####

    fig2_1 = plt.figure(figsize = (12,12))
    fig2_1.canvas.manager.set_window_title("EMA Chart")

    gs2_1 = fig2_1.add_gridspec(4,4)

    ax2_101 = fig2_1.add_subplot(gs2_1[:,0:3])
    ax2_101.set_title("%s - EMAs through %s - %s" %(ticker1name, startdate.date(), enddate.date()))
    ohlcplot(data1, ax2_101, fig2_1)
    linesPlot(ax2_101, fig2_1, data1EMA)
    ax2_101.legend()
    plotkarde2_101 = Drawer(ax2_101,fig2_1)
    
    mcursor2 = mplw.MultiCursor(fig2_1.canvas, [ax2_101] , horizOn= True, color = "lightskyblue" , linewidth = 1)
    fig2_1.tight_layout()


    #### -- E.O. EMA Chart -- ####






    #### -- Fast EMA 1st and 2nd Differential Chart -- ####

    fig5_1 = plt.figure(figsize = (12,12))
    fig5_1EMA = 10
    fig5_1.canvas.manager.set_window_title("1st and 2nd Differential %sEMA through %s - %s" %(fig5_1EMA, startdate.date(), enddate.date()))
    

    gs5_1 = fig5_1.add_gridspec(5,4)
    
    
    ax5_101 = fig5_1.add_subplot(gs5_1[0:3,0:3])
    ohlcplot(data1, ax5_101, fig5_1)
    linesPlot(ax5_101, fig5_1, data1EMA)
    plotkarde4_102 = Drawer(ax5_101,fig5_1)
    ax5_101.legend()

    
    ax5_102 = fig5_1.add_subplot(gs5_1[3:4,0:3] , sharex = ax5_101)
    ax5_102.set_title("%s - 1st Differential %sEMA through days %s - %s" %(ticker1name, fig5_1EMA, startdate.date(), enddate.date()))
    scatterPlot(ax5_102, fig5_1, data1EMASlope["%s" %(fig5_1EMA)], label = "%sEMA Slope" %(fig5_1EMA), color = "blue")
    plotkarde4_102 = Drawer(ax5_102,fig5_1)
    ax5_102.legend()


    ax5_103 = fig5_1.add_subplot(gs5_1[4:5,0:3] , sharex = ax5_101)
    ax5_103.set_title("%s - 2nd Differential (smoothed) %sEMA through days %s - %s" %(ticker1name, fig5_1EMA, startdate.date(), enddate.date()))
    scatterPlot(ax5_103, fig5_1, data1EMASlope["%s" %(fig5_1EMA)].diff().rolling(3).mean(), label = "%sEMA Diff^2" %(fig5_1EMA), color = "slateblue")
    plotkarde4_103 = Drawer(ax5_103,fig5_1)
    ax5_103.legend()
    
    mcursor5_1 = mplw.MultiCursor(fig5_1.canvas, [ax5_101,ax5_102,ax5_103] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig5_1.tight_layout()

    #### -- E.O. Fast EMA 1st and 2nd Differential Chart -- ####







    #### -- Slow EMA 1st and 2nd Differential Chart -- ####

    fig5_2 = plt.figure(figsize = (12,12))
    fig5_2EMA = 50
    fig5_2.canvas.manager.set_window_title("1st and 2nd Differential %sEMA through %s - %s" %(fig5_2EMA, startdate.date(), enddate.date()))
    

    gs5_2 = fig5_2.add_gridspec(5,4)
    
    
    ax5_201 = fig5_2.add_subplot(gs5_2[0:3,0:3])
    ohlcplot(data1, ax5_201, fig5_2)
    linesPlot(ax5_201, fig5_2, data1EMA)
    plotkarde4_202 = Drawer(ax5_201,fig5_2)

    
    ax5_202 = fig5_2.add_subplot(gs5_2[3:4,0:3] , sharex = ax5_201)
    ax5_202.set_title("%s - 1st Differential %sEMA through days %s - %s" %(ticker1name, fig5_2EMA, startdate.date(), enddate.date()))
    scatterPlot(ax5_202, fig5_2, data1EMASlope["%s" %(fig5_2EMA)], label = "%sEMA Slope" %(fig5_2EMA), color = "blue")
    plotkarde4_202 = Drawer(ax5_202,fig5_2)


    ax5_203 = fig5_2.add_subplot(gs5_2[4:5,0:3] , sharex = ax5_201)
    ax5_203.set_title("%s - 2nd Differential (smoothed) %sEMA through days %s - %s" %(ticker1name, fig5_2EMA, startdate.date(), enddate.date()))
    scatterPlot(ax5_203, fig5_2, data1EMASlope["%s" %(fig5_2EMA)].diff().rolling(3).mean(), label = "%sEMA Diff^2" %(fig5_2EMA), color = "slateblue")
    plotkarde4_203 = Drawer(ax5_203,fig5_2)
    
    mcursor5_2 = mplw.MultiCursor(fig5_2.canvas, [ax5_201,ax5_202,ax5_203] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig5_2.tight_layout()

    #### -- E.O. Slow EMA 1st and 2nd Differential Chart -- ####




    #### -- MACD Chart -- ####

    fig9 = plt.figure(figsize=(12,12))
    fig9EMAFast = 10
    fig9EMASlow = 25
    fig9EMASlowSlow = 50
    fig9.canvas.manager.set_window_title("MACD Chart")

    gs9 = fig9.add_gridspec(5,4)

    ax901 = fig9.add_subplot(gs9[0:3,0:3])
    ax901.set_title("%s - MACD through days %s - %s" %(ticker1name,startdate,enddate))    
    ohlcplot(data1, ax901, fig9)
    linesPlot(ax901, fig9, data1EMA)
    plotkarde901 = Drawer(ax901,fig9)
    ax901.legend()


    ax902 = fig9.add_subplot(gs9[3:4,0:3] , sharex = ax901)
    ax902.set_title("%s - %s - %s MACD through days %s - %s" %(ticker1name, fig9EMAFast, fig9EMASlow, startdate, enddate))    
    ax902.bar( rangedata1 , (data1EMA["%s" %(fig9EMAFast)] - data1EMA["%s" %(fig9EMASlow)]).values, color = "brown" , alpha = 0.5 , label = "MACD %s - %s" %(fig9EMAFast , fig9EMASlow) )
    ax902.axhline( int(0) , color = "red")
    ax902.legend()
    plotkarde902 = Drawer(ax902,fig9)
    ax902.legend()
    
    
    ax903 = fig9.add_subplot(gs9[4:5,0:3] , sharex = ax901)
    ax903.set_title("%s - %s - %s MACD through days %s - %s" %(ticker1name, fig9EMASlow, fig9EMASlowSlow, startdate, enddate))    
    ax903.bar( rangedata1 , (data1EMA["%s" %(fig9EMASlow)] - data1EMA["%s" %(fig9EMASlowSlow)]).values, color = "darkseagreen" , alpha = 0.5 , label = "MACD %s - %s" %(fig9EMASlow , fig9EMASlowSlow) )
    ax903.axhline( int(0) , color = "red")
    ax903.legend()
    plotkarde903 = Drawer(ax903,fig9)
    ax903.legend()


    mcursor9 = mplw.MultiCursor(fig9.canvas, [ax901,ax902,ax903] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig9.tight_layout()

    #### -- E.O. MACD Chart -- ####





    
    




    
    
    #### -- Volume Chart -- ####

    fig5_3 = plt.figure(figsize = (12,12))
    fig5_3.canvas.manager.set_window_title("Volume Chart")

    gs5_3 = fig5_3.add_gridspec(3,4)

    ax5_301 = fig5_3.add_subplot(gs5_3[0:2,0:3])
    ax5_301.set_title("%s - Volume through days %s - %s" %(ticker1name, startdate.date(), enddate.date()))
    ohlcplot(data1, ax5_301, fig5_3)
    plotkarde501 = Drawer(ax5_301,fig5_3)


    data1VolMean = data1["Volume"].loc[enddate - datetime.timedelta(days = 244):enddate].mean()
    data1VolStD = data1["Volume"].loc[enddate - datetime.timedelta(days = 244):enddate].std()
    
    ax5_302 = fig5_3.add_subplot(gs5_3[2:3,0:3] , sharex = ax5_301)
    ax5_302.bar( rangedata1 , data1["Volume"].values , label = "Volume" , color = "blue" , alpha = 0.7 )
    ax5_302.axhline( ( data1VolMean ) , color = "red" , alpha = 0.7 )
    ax5_302.axhline( ( data1VolMean + data1VolStD ) , color = "red" , alpha = 0.7 )
    ax5_302.axhline( ( data1VolMean - data1VolStD ) , color = "red" , alpha = 0.7 )    
    ax5_302.set_ylim( 0 , data1["Volume"].max() + data1["Volume"].mean()/100 )
    plotkarde502 = Drawer(ax5_302,fig5_3)


    mcursor5_3 = mplw.MultiCursor(fig5_3.canvas, [ax5_301,ax5_302] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig5_3.tight_layout()

    #### -- E.O. Volume Chart -- ####


    

    

    

    #### -- Standardized Line (Close) Chart -- ####

    fig6 = plt.figure(figsize = (12,12))
    fig6.canvas.manager.set_window_title("Standardized Line (Close) Chart")
    gs6 = fig6.add_gridspec(4,4)
    
    ax601 = fig6.add_subplot(gs6[:,0:3])
    ax601.set_title("%s - Standardized Price through days %s - %s" %(ticker1name, startdate.date(), enddate.date()))
    
    ax601.plot( rangedata1 , DataStand(data1["Close"]).values , label = "%s Standardized" %(ticker1name) , color = "silver")
    ax601.axhline( 0, color = "red" , label = "Mean for time period" )
    cursor601 = mplw.Cursor(ax601 , useblit=True, color = "lightskyblue" , linewidth = 1)
    plotkarde601 = Drawer(ax601,fig6)
    ax601.legend()
    
    mcursor6 = mplw.MultiCursor(fig6.canvas, [ax601] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig6.tight_layout()

    #### -- E.O. Standardized Line (Close) Chart -- ####
    
    
    

    


    #### -- RSI Chart -- ####    

    fig7 = plt.figure(figsize = (12,12))
    fig7.canvas.manager.set_window_title("RSI Index")
    
    gs7 = fig7.add_gridspec(10,4)
    
    
    ax701 = fig7.add_subplot(gs7[0:7,0:3])
    ax701.set_title("%s - RSI Index through days %s - %s" %(ticker1name, startdate.date(), enddate.date()))
    ohlcplot(data1, ax701, fig7)
    plotkarde701 = Drawer(ax701,fig7)
    
    
    ax702 = fig7.add_subplot(gs7[7:10,0:3] , sharex = ax701)
    
    data1RSIMean = data1RSI["RSI"].mean()
    data1RSIStD = data1RSI["RSI"].std()

    ax702.plot( range(data1RSI.index.size) , data1RSI["RSI"] , label = "RSI" , color = "blue" )
    ax702.axhline( data1RSIMean  , label = "RSI Mean" , color = "red" )
    ax702.axhline( ( data1RSIMean + 2*data1RSIStD ) , color = "green" )
    ax702.axhline( ( data1RSIMean - 2*data1RSIStD ) , color = "green" )
    ax702.axhline( 20 , color = "lime" )
    ax702.axhline( 80 , color = "lime" )
    ax702.set_ylim( -10 , 110 )
    plotkarde702 = Drawer(ax702,fig7)
    
    
    mcursor7 = mplw.MultiCursor(fig7.canvas, [ax701,ax702] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig7.tight_layout()

    #### -- E.O. RSI Chart -- ####    







    #### -- Bollinger Band -- ####

    fig10 = plt.figure(figsize=(12,12))
    fig10.canvas.manager.set_window_title("Bollinger Bands")
    gs10 = fig10.add_gridspec(5,4)

    ax1001 = fig10.add_subplot(gs10[:,0:3])
    ax1001.set_title("%s - Bollinger Bands through days %s - %s" %(ticker1name, startdate.date(), enddate.date()))
    ohlcplot(data1, ax1001, fig10)
    ax1001.plot( rangedata1 , data1BB["1STDUP"] , color = "darkblue" , alpha = 0.5)
    ax1001.plot( rangedata1 , data1BB["1STDDN"] , color = "darkorange" , alpha = 0.5)
    ax1001.plot( rangedata1 , data1BB["2STDUP"] , color = "cadetblue" , alpha = 0.5)
    ax1001.plot( rangedata1 , data1BB["2STDDN"] , color = "sandybrown" , alpha = 0.5)
    plotkarde1001 = Drawer(ax1001,fig10)

    mcursor10 = mplw.MultiCursor(fig10.canvas, [ax1001] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    fig10.tight_layout()

    #### -- E.O. Bollinger Band -- ####




    """









    #    #### -- DMA 1st Differential Chart -- ####
    #
    #
    #    fig3 = plt.figure(figsize=(12,12))
    #    fig3.canvas.manager.set_window_title("1st Differential")
    #    gs3 = fig3.add_gridspec(12,4)
    #    
    #    fig3DMAFast = 10
    #    fig3DMASlow = 50
    #
    #    
    #    ax301 = fig3.add_subplot(gs3[0:8,0:3])
    #    ax301.set_title("%s - 1st Differential DMAs through %s - %s" %(ticker1name, startdate.date(), enddate.date()))
    #    linesPlot(ax301, fig3, data1DMA)
    #    ohlcplot(data1, ax301, fig3)
    #    ax301.legend()
    #    plotkarde301 = Drawer(ax301,fig3)
    #
    #
    #    ax302 = fig3.add_subplot(gs3[8:10,0:3] , sharex = ax301)
    #    scatterPlot(ax302, fig3, data1DMASlope['%s' %(fig3DMAFast)], label= "%s" %(fig3DMAFast), color = "blue")
    #    scatterPlot(ax302, fig3, data1DMASlope['%s' %(fig3DMASlow)], label= "%s" %(fig3DMASlow), color = "green")
    #    ax302.legend()
    #    plotkarde302 = Drawer(ax302,fig3)
    #    
    #    
    #    ax303 = fig3.add_subplot(gs3[10:12,0:3] , sharex = ax301)
    #    scatterPlot(ax303, fig3, data1DMASlope['%s' %(fig3DMAFast)] - data1DMASlope['%s' %(fig3DMASlow)], label= "%s-%s" %(fig3DMAFast, fig3DMASlow), color = "firebrick")
    #    plotkarde303 = Drawer(ax303,fig3)
    #    ax303.legend()
    #
    #    
    #    mcursor3 = mplw.MultiCursor(fig3.canvas, [ax301,ax302,ax303] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    #    fig3.tight_layout()
    #
    #    #### -- E.O. DMA 1st Differential Chart -- ####
    

    
    
    
    

    #    #### -- DMA 2nd Differential Chart -- ####
    #
    #    fig4 = plt.figure(figsize = (12,12))
    #    fig4.canvas.manager.set_window_title("2nd Differential")
    #
    #    gs4 = fig4.add_gridspec(7,4)
    #
    #    fig4DMAFast = 10
    #    fig4DMASlow = 50
    #    
    #    
    #    ax401 = fig4.add_subplot(gs4[0:4,0:3])
    #    ax401.set_title("%s - 2nd Differential %sDMA & %sDMA through %s - %s" %(ticker1name, fig4DMAFast, fig4DMASlow, startdate.date(), enddate.date()))
    #
    #    ohlcplot(data1, ax401, fig4)
    #    linesPlot(ax401, fig4, data1DMA)
    #    ax401.legend()
    #    plotkarde401 = Drawer(ax401,fig4)
    #
    #
    #    ax402 = fig4.add_subplot(gs4[4:7,0:3] , sharex = ax401)
    #    scatterPlot(ax402, fig4, data1DMASlope["%s" %(fig4DMAFast)].diff(), label = "%sDMA Diff^2" %(fig4DMAFast) , color = "blue")    
    #    scatterPlot(ax402, fig4, data1DMASlope["%s" %(fig4DMASlow)].diff(), label = "%sDMA Diff^2" %(fig4DMASlow) , color = "green")
    #    ax402.legend()
    #    plotkarde402 = Drawer(ax402,fig4)
    #
    #
    #
    #    mcursor4 = mplw.MultiCursor(fig4.canvas, [ax401,ax402] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    #    fig4.tight_layout()
    #
    #    #### -- E.O. DMA 2nd Differential Chart -- ####


    

    #    fig5_1 = plt.figure(figsize = (12,12))
    #    gs = fig5_1.add_gridspec(6,4)
    #    
    #    ax5_101 = fig5_1.add_subplot(gs[0:3,0:3])
    #    ax5_101.set_title("Volume  %s through %s days %s - %s" %(ticker1name,data1size,startdate,enddate))
    #
    #    ohlcplot(ax5_101)
    #
    #    cursor5_101 = mplw.Cursor(ax5_101 , useblit=True, color = "lightskyblue" , linewidth = 1)
    #
    #    marginandstuff()
    #
    #    plotkarde5_101 = Drawer(ax5_101,fig5_1)
    #
    #    ax5_102 = fig5_1.add_subplot(gs[3:4,0:3] , sharex = ax5_101)
    #
    #    ax5_102.bar( data1.index , data1["Volume"] , label = "%s Volume" %(ticker1name) , color = "blue" , alpha = 0.7 )
    #    ax5_102.axhline( ( data1["Volume"].loc[enddate - datetime.timedelta(days = 244):enddate].mean() ) , color = "violet" , alpha = 0.7 )
    #    ax5_102.axhline( ( (data1["Volume"].max() + data1["Volume"].min())/2 ) , color = "green" , alpha = 0.7 )
    #    ax5_102.axhline( ( data1["Volume"].loc[enddate - datetime.timedelta(days = 244):enddate].mean() + data1["Volume"].loc[enddate - datetime.timedelta(days = 244):enddate].std() ) , color = "red" , alpha = 0.7 )
    #    ax5_102.axhline( ( data1["Volume"].loc[enddate - datetime.timedelta(days = 244):enddate].mean() - data1["Volume"].loc[enddate - datetime.timedelta(days = 244):enddate].std() ) , color = "red" , alpha = 0.7 )
    #    
    #    ax5_102.set_ylim( 0 , data1["Volume"].max() + data1["Volume"].std() )
    #    
    #    marginandstuffforx()
    #
    #
    #    ax5_103 = fig5_1.add_subplot(gs[4:5,0:3] , sharex = ax5_101)
    #
    #    ax5_103.bar( data1_ohcl_low_vol.index , data1_ohcl_low_vol["Volume"] , label = "%s Low Volume" %(ticker1name) , color = "blue" , alpha = 0.7 )
    #    ax5_103.axhline( data1_ohcl_low_vol["Volume"].mean() , color = "violet" , alpha = 0.7 )
    #    ax5_103.axhline( ( data1_ohcl_low_vol["Volume"].max() + data1_ohcl_low_vol["Volume"].min())/2 , color = "green" , alpha = 0.7 )
    #    ax5_103.axhline( ( data1_ohcl_low_vol["Volume"].mean() + data1_ohcl_low_vol["Volume"].std() ) , color = "red" , alpha = 0.7 )
    #    ax5_103.axhline( ( data1_ohcl_low_vol["Volume"].mean() - data1_ohcl_low_vol["Volume"].std() ) , color = "red" , alpha = 0.7 )
    #    
    #    ax5_103.set_ylim( 0 , data1["Volume"].max() + data1["Volume"].std() )
    #    
    #    marginandstuffforx()
    #
    #
    #    ax5_104 = fig5_1.add_subplot(gs[5:6,0:3] , sharex = ax5_101)
    #
    #    ax5_104.bar( data1_ohcl_high_vol.index , data1_ohcl_high_vol["Volume"] , label = "%s Low Volume" %(ticker1name) , color = "blue" , alpha = 0.7 )
    #    ax5_104.axhline( data1_ohcl_high_vol["Volume"].mean() , color = "violet" , alpha = 0.7 )
    #    ax5_104.axhline( (data1_ohcl_high_vol["Volume"].max() + data1_ohcl_high_vol["Volume"].min())/2 , color = "green" , alpha = 0.7 )
    #    ax5_104.axhline( ( data1_ohcl_high_vol["Volume"].mean() + data1_ohcl_high_vol["Volume"].std() ) , color = "red" , alpha = 0.7 )
    #    ax5_104.axhline( ( data1_ohcl_high_vol["Volume"].mean() - data1_ohcl_high_vol["Volume"].std() ) , color = "red" , alpha = 0.7 )
    #    
    #    ax5_104.set_ylim( 0 , data1["Volume"].max() + data1["Volume"].std() )
    #    
    #    marginandstuffforx()
    #    
    #    fig5_1.tight_layout()
    #
    #    fig5_1.canvas.manager.set_window_title("Detailed Volume Chart")
    #
    #    mcursor5 = mplw.MultiCursor(fig5_1.canvas, [ax5_101, ax5_102, ax5_103, ax5_104] , horizOn= True , color = "lightskyblue" , linewidth = 1)

    #    #### -- EMA 2nd Differential Chart -- ####
    #
    #    fig5 = plt.figure(figsize = (12,12))
    #    fig5.canvas.manager.set_window_title("2nd Differential EMA")
    #
    #    gs5 = fig5.add_gridspec(7,4)
    #
    #    fig5EMAFast = 10
    #    fig5EMASlow = 50
    #    
    #    
    #    ax501 = fig5.add_subplot(gs5[0:4,0:3])
    #    ax501.set_title("2nd Differential 10EMA & 50EMA %s through %s - %s" %(ticker1name, startdate.date(), enddate.date()))
    #
    #    ohlcplot(data1, ax501, fig5)
    #    linesPlot(ax501, fig5, data1EMA)
    #    ax501.legend()
    #    plotkarde401 = Drawer(ax501,fig5)
    #
    #
    #    ax502 = fig5.add_subplot(gs5[4:7,0:3] , sharex = ax501)
    #    scatterPlot(ax502, fig5, data1EMA["%s" %(fig5EMAFast)].diff(), label = "%sEMA Diff^2" %(fig5EMAFast) , color = "blue")    
    #    scatterPlot(ax502, fig5, data1EMA["%s" %(fig5EMASlow)].diff(), label = "%sEMA Diff^2" %(fig5EMASlow) , color = "green")
    #    ax502.legend()
    #    plotkarde402 = Drawer(ax502,fig5)
    #
    #
    #    mcursor5 = mplw.MultiCursor(fig5.canvas, [ax501,ax502] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    #    fig5.tight_layout()
    #
    #    #### -- E.O. EMA 2nd Differential Chart -- ####




    """





    pass

except:
    
    print(traceback.print_exc())
    input("\nError BC.\n")



end = time.time()
print("Total time taken by program = " , end - start)
print("\n\n\n")



plotshowkar()



#
    #   try:
    #       pdf = PdfPages("D:\Finance\Stocks\Company Data\Recent\%s\%s_%s_%sdays.pdf" %( ticker1name , ticker1name , startdate , enddate ))
    #       pdf.savefig(fig1)
    #       pdf.savefig(fig2)
    #       pdf.savefig(fig3)
    #       pdf.savefig(fig4)
    #       pdf.savefig(fig5)
    #       pdf.savefig(fig6)
    #       pdf.savefig(fig7)
    #       pdf.savefig(fig8)
    #       pdf.savefig(fig9)
    #       
    #       pdf.close()
    #   
    #   except Exception as exp:
    #       print(exp)
    #       input()
#




#### -- Graphing and plotting done -- ####



#input("End")



try:

    pass
    #code.interact(local = locals())

except:
    
    print(traceback.print_exc())
    input("\nError BC.\n")












try:



    
    """
    
    root = tk.Tk()
    
    #"""



    """
    
    mainframe = tk.Frame(root)
    mainframe.grid(row = 0, column = 0, sticky = "nsew")
    
    #"""



    """
    
    fig1 = mpl.figure.Figure(figsize = (5,5))
    ax101 = fig1.add_subplot()
    ax101.set_title("OHLC chart for time period %s to %s " %(startdate , enddate))

    ohlcplot(ax101)
    
    marginandstuff(ax101,fig1)
    
    
    mcursor101 = mplw.MultiCursor(fig1.canvas , [ax101] , horizOn= True , color = "lightskyblue" , linewidth = 1)
    
    #"""
        
    """

    fig1tk = FigureCanvasTkAgg(fig1, root)
    fig1tk.get_tk_widget().grid(row = 0 , column = 0 , sticky="nsew" )
    root.grid_rowconfigure(0 , weight = 100)
    root.grid_columnconfigure(0 , weight = 100)
    
    #"""
    
    """
    
    fig1tktb = NavigationToolbar2Tk(fig1tk , root , pack_toolbar=False)
    fig1tktb.grid(row = 1 , column = 0 , sticky="nsew" )
    root.grid_rowconfigure(1 , weight = 1)
    root.grid_columnconfigure(0 , weight = 1)
    
    fig1tktb.update()
    
    #"""

    #plotkardefig1 = Drawer(ax101,fig1,fig1tk)


    
    
    """
    
    fig2 = mpl.figure.Figure(figsize = (12,12))

    gs = fig2.add_gridspec(10,10)

    ax201 = fig2.add_subplot(gs[:,:])

    ax201.set_title("%s through %s days (recent) %s - %s Rolling Mean 10-50-100" %(ticker1name,data1size,startdate,enddate))
    
    ohlcplot(ax201)
    
    ax201.plot( data1.index , data1["Close"].rolling(window = 10).mean() , label = "%s 10" %(ticker1name) , color = "blue" , alpha = 0.7)
    ax201.plot( data1.index , data1["Close"].rolling(window = 25).mean() , label = "%s 25" %(ticker1name) , color = "skyblue" , alpha = 0.7)
    ax201.plot( data1.index , data1["Close"].rolling(window = 50).mean() , label = "%s 50" %(ticker1name) , color = "green" , alpha = 0.7)
    ax201.plot( data1.index , data1["Close"].rolling(window = 100).mean() , label = "%s 100" %(ticker1name) , color = "orchid" , alpha = 0.7)
    ax201.plot( data1.index , data1["Close"].rolling(window = 200).mean() , label = "%s 200" %(ticker1name) , color = "gold" , alpha = 0.7)
    
    
    marginandstuff(ax201,fig2)
    

    mcursor201 = mplw.MultiCursor(fig2.canvas, [ax201] , horizOn= True, color = "lightskyblue" , linewidth = 1)

    #"""
    
    """
    
    fig2tk = FigureCanvasTkAgg(fig2, root)
    fig2tk.get_tk_widget().grid(row = 0 , column = 1 , sticky="nsew" )
    root.grid_rowconfigure(0 , weight = 100)
    root.grid_columnconfigure(1 , weight = 100)
    
    #"""
    
    """

    fig2tktb = NavigationToolbar2Tk(fig2tk , root , pack_toolbar=False)
    fig2tktb.grid(row = 1 , column = 1 , sticky="nsew" )
    root.grid_rowconfigure(1 , weight = 1)
    root.grid_columnconfigure(1 , weight = 1)
    fig2tktb.update()
    
    #"""
    
    #plotkardefig2 = Drawer(ax201,fig2,fig2tk)
    
    """
    
    root.mainloop()
    
    #"""



    pass



except:
    
    print(traceback.print_exc())
    input("\nError BC.\n")
