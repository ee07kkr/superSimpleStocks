#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 23:31:31 2018
@desc: base class to be imported to main code.
@author: krewari
"""
from __future__ import division
from datetime import datetime
import time
#Inheriting error class to create new error type - Dependency error.
class Error(Exception):
    pass
class DependencyError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
#getter/setter along with a decorator to check attribute's type.
def get_set_gen(name, type_):
    def getter(self):
        return getattr(self, "__" + name)
    def setter(self, value):
        if not isinstance(value, type_):
            raise TypeError("%s attribute must be set to an instance of %s" % (name, type_))
        setattr(self, "__" + name, value)
    return property(getter, setter)
#function that will act as decorator to the stock class.
def auto_attr_check(cls_obj):
    new_dict = {}
    for key, value in cls_obj.__dict__.items():
        if isinstance(value, type):
            value = get_set_gen(key, value)
        new_dict[key] = value
    # Creates a new class, using the modified dictionary as the class dict:
    return type(cls_obj)(cls_obj.__name__, cls_obj.__bases__, new_dict)

@auto_attr_check
class stock():
    ticker = str
    stock_type = str
    par_value = float
    last_div = float
#Initilialising stock object attributes 
    def __init__(self, ticker, stock_type, last_div, fix_div, par_value):
        """ticker,stock_type,fix_div must be entered as string; last_div and par_value can be int/float"""
        self.ticker = ticker.strip()
        self.stock_type = stock_type.strip()
        self.last_div = float(last_div.strip())
        self.par_value = float(par_value.strip())
        self.trades = []
        try:
            self.fix_div = float((fix_div.strip('%').strip()))/100 if fix_div.strip() not in ('None', 'none', None, '') else None
        except:
            raise TypeError("Fixed Dividend options - x%,None,none,blank")  
        if(self.stock_type.lower().strip() not in ['common', 'preferred']):
            raise ValueError("stock_type can only take one of two values - common or preferred")
        if(self.stock_type.lower().strip() == 'preferred' and self.fix_div is None):
            raise DependencyError("InputError:", "Incase of preferred stock, provide Fixed Dividend")
#function to record trade for a stock object
    def record_trade(self, shares, trade_type, price, timestamp=(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')):
        """Timestamp must be entered as a string in following format - %Y-%m-%d %H:%M:%S """
        try:
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            shares = float(shares)
            price = float(price)
        except:
            raise TypeError("Shares,Price must be float/integer & timestamp in YYYY-mm-dd HH:MM:SS format")
        if(trade_type.lower() not in ['buy', 'sell']):
            raise ValueError("trade_type can only take one of two values - Buy or Sell")
        print('****************TRADE(S) RECORDED****************\n')
        self.trades.append([self.ticker, trade_type, shares, price, timestamp])
#function to calculate avg. stock price based of last 15mins trades
    def stock_price_cal(self):
        total_market_cap15 = 0
        total_vol_15 = 0
        if len(self.trades) > 0:
            for trade in self.trades:
                if int(time.mktime(datetime.now().timetuple()) - time.mktime(trade[4].timetuple())) <= 900:
                    total_market_cap15 += (trade[2]*trade[3])
                    total_vol_15 += trade[2]
            if total_vol_15 > 0:
                return total_market_cap15/total_vol_15
            else:
                print("No trade found for {k} in the last 15 minutes. \n".format(k=self.ticker))
        else:
            print("No trades for {k} found at all.\n".format(k=self.ticker))
#function to calculate avg.stock price based of last 24hrs
    def stock_price_cal_for_index(self):
        total_market_cap24h = 0
        total_vol_24h = 0
        if len(self.trades) > 0:
            for trade in self.trades:
                if int(time.mktime(datetime.now().timetuple()) - time.mktime(trade[4].timetuple())) <= 86400: #24hrs
                    total_market_cap24h += (trade[2]*trade[3])
                    total_vol_24h += trade[2]
            if total_vol_24h > 0:
                return total_market_cap24h/total_vol_24h
            else:
                print("No trade found for {k} in the last 24 hrs\n".format(k=self.ticker))
        else:
            print("No trades for {k} found at all\n".format(k=self.ticker))
#function to calculate dividend yield
    def dividend_yield(self, ticker_price=None):
        """Ticker Price must be a float or int and denominated in pennies."""
        if self.stock_type.lower().strip() == 'common':
            return self.last_div/ticker_price
        elif self.stock_type.lower().strip() == 'preferred':
            return (self.fix_div*self.par_value)/ticker_price
#function to calculate pe ratio
    def pe_ratio(self, ticker_price=None):
        """Ticker Price must be a float or int and denominated in pennies"""
        if self.last_div > 0:
            return ticker_price/self.last_div
        else:
            print("Last Dividend for {qq} is 0\n".format(qq=self.ticker))
