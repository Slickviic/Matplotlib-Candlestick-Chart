import pandas as pd
import mplfinance as mpf
import yfinance as yf
import pandas_ta as pdta
from dateutil import tz
import matplotlib.pyplot as plt
import matplotlib as mpl
from yfinance import ticker
from datetime import datetime, timedelta, date


def utc_to_local(date_time_list):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    for i  in range(0, len(date_time_list)):

        # Get utc time
        utc = date_time_list[i]

        # Tell the datetime object that it's in UTC time zone since 
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        local = utc.astimezone(to_zone)

        date_time_list[i] = local


    return date_time_list

def start_date(time_interval):
    '''
    Definition: Determines the start date that gives 100 bars in length given a time interval.

    Paramters:
    time_interval (str): A viable time interval taken by Yahoo Finance

    Returns (str): Start time
    '''
    current_date = date.today()
    multiple = 100.0

    if time_interval == '1w':
        return current_date - timedelta(weeks = multiple)

    elif time_interval == '1d':
        return current_date - timedelta(days = multiple)

    elif time_interval == '1h':
        return current_date - timedelta(hours = multiple)

    elif time_interval == '30m':
        multiple *= 30
        return current_date - timedelta(minutes = multiple)

    elif time_interval == '15m':
        multiple *= 15
        return current_date - timedelta(minutes = multiple)

    elif time_interval == '5m':
        multiple *= 5
        return current_date - timedelta(minutes = multiple)

    elif time_interval == '1m':
        return current_date - timedelta(minutes = multiple)



ticker_name = "ETH-USD"

mtf_interval = '1wk'

ltf_interval = '1d'


#Get Ticker Data


mtf_df = yf.Ticker(ticker_name).history(period="max", interval=mtf_interval, start = start_date(mtf_interval))

ltf_df = yf.Ticker(ticker_name).history(period="max", interval=ltf_interval, start = start_date(ltf_interval))


#Calculate MACD/EMA values MFT
macd_mtf = pdta.macd(close = mtf_df['Close'])
ema_30_mtf = pdta.ema(close = mtf_df['Close'], length = 30)
ema_60_mtf = pdta.ema(close = mtf_df['Close'], length = 60)
ema_365_mtf = pdta.ema(close = mtf_df['Close'], length = 365)

#Calculate MACD/EMA values LFT
macd_ltf = pdta.macd(close = ltf_df['Close'])
ema_30_ltf = pdta.ema(close = ltf_df['Close'], length = 30)
ema_60_ltf = pdta.ema(close = ltf_df['Close'], length = 60)
ema_365_ltf = pdta.ema(close = ltf_df['Close'], length = 365)



#Append indicator values to Data Frame MTF
mtf_df['MACD_12_26_9'] = macd_mtf['MACDh_12_26_9']
mtf_df['EMA_30'] = ema_30_mtf
mtf_df['EMA_60'] = ema_60_mtf
mtf_df['EMA_365'] = ema_365_mtf

#Append indicator values to Data Frame LTF
ltf_df['MACD_12_26_9'] = macd_ltf['MACDh_12_26_9']
ltf_df['EMA_30'] = ema_30_ltf
ltf_df['EMA_60'] = ema_60_ltf
ltf_df['EMA_365'] = ema_365_ltf



#Convert UTC df index into a list and convert the list to local time MTF
date_list_mtf = utc_to_local(mtf_df.index.tolist())

#Convert UTC df index into a list and convert the list to local time LTF
date_list_ltf = utc_to_local(ltf_df.index.tolist())



#Create new Date column and set it to index
mtf_df['Date'] = date_list_mtf

mtf_df['Date'] = pd.to_datetime(mtf_df['Date'], format = "%y/%m/%d, %H:%M:%S")

mtf_df = mtf_df.set_index('Date')

#Create new Date column and set it to index
ltf_df['Date'] = date_list_ltf

ltf_df['Date'] = pd.to_datetime(ltf_df['Date'], format = "%y/%m/%d, %H:%M:%S")

ltf_df = ltf_df.set_index('Date')



#define grid of plots
fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=False)

#rotate x-axis tick labels
axs[1][0].tick_params(axis='x', labelrotation = 45)
axs[1][1].tick_params(axis='x', labelrotation = 45)



#add title and axes labels
label_kwargs = {
    'fontsize' : 'small'}

#MTF Figure
axs[0][0].set_title(ticker_name + ' ' + mtf_interval.upper(), label_kwargs)
axs[1][0].set_title('MACD 12 26 9', label_kwargs)

axs[0][0].set_ylabel('Price', label_kwargs)
axs[1][0].set_ylabel('MACD 12 26 9 Values', label_kwargs)

axs[0][0].set_xlabel('Date', label_kwargs)

axs[0][0].set_facecolor('#ffffff')
axs[1][0].set_facecolor('#ffffff')

axs[0][0].grid(visible = True)
axs[1][0].grid(visible = True)

#LTF Figure
axs[0][1].set_title(ticker_name + ' ' + ltf_interval.upper(), label_kwargs)
axs[1][1].set_title('MACD 12 26 9', label_kwargs)

axs[0][1].set_ylabel('Price', label_kwargs)
axs[1][1].set_ylabel('MACD 12 26 9 Values', label_kwargs)

axs[0][1].set_xlabel('Date', label_kwargs)

axs[0][1].set_facecolor('#ffffff')
axs[1][1].set_facecolor('#ffffff')

axs[0][1].grid(visible = True)
axs[1][1].grid(visible = True)



#define up and down prices MTF
up_mtf = mtf_df[mtf_df.Close>=mtf_df.Open]

down_mtf = mtf_df[mtf_df.Close<mtf_df.Open]

#define up and down prices LTF
up_ltf = ltf_df[ltf_df.Close>=ltf_df.Open]

down_ltf = ltf_df[ltf_df.Close<ltf_df.Open]

#define width of candlestick elements
width = .75
width2 = .05

#define colors to use
col1 = 'green'
col2 = 'red'



#plot up prices MTF
axs[0][0].bar(up_mtf.index, up_mtf.Close-up_mtf.Open,width,bottom=up_mtf.Open,color=col1)
axs[0][0].bar(up_mtf.index,up_mtf.High-up_mtf.Close,width2,bottom=up_mtf.Close,color=col1)
axs[0][0].bar(up_mtf.index,up_mtf.Low-up_mtf.Open,width2,bottom=up_mtf.Open,color=col1)

#plot up prices LTF
axs[0][1].bar(up_ltf.index, up_ltf.Close-up_ltf.Open,width,bottom=up_ltf.Open,color=col1)
axs[0][1].bar(up_ltf.index,up_ltf.High-up_ltf.Close,width2,bottom=up_ltf.Close,color=col1)
axs[0][1].bar(up_ltf.index,up_ltf.Low-up_ltf.Open,width2,bottom=up_ltf.Open,color=col1)

#plot down prices MTF
axs[0][0].bar(down_mtf.index,down_mtf.Close-down_mtf.Open,width,bottom=down_mtf.Open,color=col2)
axs[0][0].bar(down_mtf.index,down_mtf.High-down_mtf.Open,width2,bottom=down_mtf.Open,color=col2)
axs[0][0].bar(down_mtf.index,down_mtf.Low-down_mtf.Close,width2,bottom=down_mtf.Close,color=col2)

#plot down prices LTF
axs[0][1].bar(down_ltf.index,down_ltf.Close-down_ltf.Open,width,bottom=down_ltf.Open,color=col2)
axs[0][1].bar(down_ltf.index,down_ltf.High-down_ltf.Open,width2,bottom=down_ltf.Open,color=col2)
axs[0][1].bar(down_ltf.index,down_ltf.Low-down_ltf.Close,width2,bottom=down_ltf.Close,color=col2)



#plot EMAs MTF
ema_30 = axs[0][0].plot(mtf_df.index, mtf_df.EMA_30, 'g', linewidth = 0.5)
ema_60 = axs[0][0].plot(mtf_df.index, mtf_df.EMA_60, 'y', linewidth = 0.5)
ema_365 = axs[0][0].plot(mtf_df.index, mtf_df.EMA_365, 'r')

#plot EMAs LTF
ema_30 = axs[0][1].plot(ltf_df.index, ltf_df.EMA_30, 'g', linewidth = 0.5)
ema_60 = axs[0][1].plot(ltf_df.index, ltf_df.EMA_60, 'y', linewidth = 0.5)
ema_365 = axs[0][1].plot(ltf_df.index, ltf_df.EMA_365, 'r')



#Plot MACD MTF
macd_up_mtf = mtf_df[mtf_df.MACD_12_26_9>=0]
macd_down_mtf = mtf_df[mtf_df.MACD_12_26_9<0]

axs[1][0].axhline(0, color = 'black')

axs[1][0].bar(macd_up_mtf.index, height = macd_up_mtf.MACD_12_26_9, width = width, bottom = 0, color = col1)
axs[1][0].bar(macd_down_mtf.index, height = macd_down_mtf.MACD_12_26_9, width = width, bottom = 0, color=col2)

#Plot MACD LTF
macd_up_ltf = ltf_df[ltf_df.MACD_12_26_9>=0]
macd_down_ltf = ltf_df[ltf_df.MACD_12_26_9<0]

axs[1][1].axhline(0, color = 'black')

axs[1][1].bar(macd_up_ltf.index, height = macd_up_ltf.MACD_12_26_9, width = width, bottom = 0, color = col1)
axs[1][1].bar(macd_down_ltf.index, height = macd_down_ltf.MACD_12_26_9, width = width, bottom = 0, color=col2)


#display candlestick chart
plt.show()
