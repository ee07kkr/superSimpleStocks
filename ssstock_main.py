#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Ticker Price check needs to be done here
"""
Created on Thu Oct  4 23:35:50 2018
@desc: main source code that calls the base class stock
@author: krewari
"""
from __future__ import division
import csv
from ssstock_class import stock

#Initialising stock dictionary with default entries
stock_list = {}
# function that provides stock analysis data
def stock_analysis(stockname):
    while True:
        try:
            tickp = float(input('Enter a ticker price in pennies or 999 to use average stock Price of last 15mins trade:  \n'))
            if tickp == 999.0:
                tickp = float(stock_list[stockname].stock_price_cal())
        except:
            print("We need a ticker price that is floating or integer datatype.\n")
            continue
        else:
            print('Dividend Yield for ticker {a} is:  {b} \n'.format(a=stock_list[stockname].ticker, b=stock_list[stockname].dividend_yield(tickp)))
            print('P/E ratio of the ticker {c} is:  {d} \n'.format(c=stock_list[stockname].ticker, d=stock_list[stockname].pe_ratio(tickp)))
            print('Average price of ticker {e} over last 15 mins is:  {f} \n'.format(e=stock_list[stockname].ticker, f=stock_list[stockname].stock_price_cal()))
            break
# function to manually enter trade details - if no csv file can be provided.
def trade_entry(stockname):
    while True:
        try:
            trade_details = str(input("Comma-seperated details in following order: \
                                       Shares Traded,Trade Type, Trade Price, timestamp(optional:if not provided, defaults to current time)\n"))
            trade_list = [item for item in trade_details.split(',')]
            stock_list[stockname].record_trade(*trade_list)
            more_trades = str(input("Do you want to enter more trades for this ticker? Yes or No\n"))
            if more_trades.lower() in ('yes', 'y'):
                trade_entry(stockname)
        except:
            print("Make sure the order is shares,tradetype, price, timestamp -as a string in format YYYY-mm-dd HH:MM:SS\n")
            print("Do not put a comma after price if timestamp is not being provided\n")
            continue
        else:
            break
#function to automatically enter multiple trades for ticker whose stock object exists
def multiple_trade_entry():
    try:
        xreader = csv.reader(open('multiple_trade_entry.csv', 'r'))
        for xrow in xreader:
            if (any(xrow) and (xrow[0] in stock_list.keys()) and not xrow[0].strip().startswith('#')):
                xxrow = xrow[1:]
                stock_list[xrow[0]].record_trade(*xxrow)
            elif(xrow[0] not in stock_list.keys() and not xrow[0].strip().startswith('#')):
                print("Trade Details for {ll} not recorded as no stock object for it found\n".format(ll=xrow[0]))
    except:
        print("Make sure the order is ticker,shares,tradetype, price, optional timestamp - in format YYYY-mm-dd HH:MM:SS adn retry\n")
#function to calculate GBCE Share Price Index
def calc_index():
    count = 0
    index_price = 1
    stk_price = None
    for stk in stock_list.keys():
        try:
            stk_price = float(stock_list[stk].stock_price_cal())
        except:
            try:
                print("Looking for trades in last 24hrs for avg. {p}'s stock price calc\n".format(p=stk))
                stk_price = float(stock_list[stk].stock_price_calForIndex())
            except:
                try:
                    stk_price = float(input("Enter {ww} stock price for index calculation..non-float/int entry will eliminate the stock from calculation\n".format(ww=stk)))
                except:
                    print("Stock price entered not float/int type...ignoring {p} in index calc\n".format(p=stk))
        if(stk_price and isinstance(stk_price, float)):
            count += 1
            index_price *= stk_price
    if count > 0:
        print("GBCE All Share Index value is {q}\n".format(q=index_price**(1/count)))
        return index_price**(1/count)
    else:
        print("Not enough data to calculate GBCE All Share index")
#function to manually create new stock object
def add_new_stock():
    new_stock_detail = str(input("Please enter a comma-seperated stock details in following order: \
                                Ticker Name, Common/Preferred, Last Dividend, Fix Dividend (type None or none for common stock),Par Value)\n"))
    new_stock_data = [item for item in new_stock_detail.split(',')]
    stock_list[new_stock_data[0]] = stock(*new_stock_data)
    more_new_stocks = str(input("Do you want to enter more new Stock Data? Yes or No\n"))
    if more_new_stocks.lower() in ('yes', 'y'):
        add_new_stock()
#default function that runs when the script is execution to provide user options        
def lets_run():
    print("Option 1: Stock Analysis")
    print("Option 2: Single/Manual Trade Data entry for a ticker")
    print("Option 3: Multiple Trades Entry")
    print("Option 4: Calculate GBCE share index")
    print("Option 5: Quit the code")
    prompt = None
    prompt_output = {1:stock_analysis, 2:trade_entry, 3:multiple_trade_entry, 4:calc_index}
    while prompt not in (1, 2, 3, 4, 5):
        try:
            prompt = int(input('Please enter 1, 2,3,4, or 5: \n'))
        except:
            print("Wrong entry")
            continue
        else:
            if prompt in (1, 2):
                stockname = str(input('Please provide a stock/ticker name:  \n'))
                if stockname in stock_list.keys():
                    prompt_output[prompt](stockname)
                else:
                    new_stock = str(input('Stock not found........do you want to add new stock details - Yes or No?\n'))
                    if new_stock.lower() in ('yes', 'y'):
                        add_new_stock()
            elif prompt in (3, 4):
                prompt_output[prompt]()
            else:
                break
#initilisation code that takes default data from a stock_initialisation.csv file.
if __name__ == "__main__":
    reader = csv.reader(open('stock_initialisation.csv', 'r'))
    for row in reader:
        if any(row) and not row[0].strip().startswith('#'):
            stock_list[row[0]] = stock(*row)
    lets_run()
