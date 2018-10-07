Super Simple Stocks:

The repository contains ssstock_class and ssstock_main module. ssstock_class.py is the base class where all the basic functionalities such as dividend yield, pe ratio etc. are defined.This base class is imported in the ssstock_main module, which essentially has functions to perform analysis and/or record data.

Apart from the executables, there are two csv's -  

stock_initialisation.csv : This file contains the default data that was originally provided in the case. However, this can manipulated (extra data can be added) for automation, scaling and to test the functionality.

multiple_trade_entry.csv: This file also helps in automation, scaling if multiple trade data for multiple tickers needs to be recorded.
However, please note that if a ticker is not know (stock object does not exist) or commented out, its data will be ignored.

While the two csv's can be benficial, there are function in the code that can take in manual entry - trade_entry() and add_new_stock().

Assumption:
1. In my understanding Ticker Price and Stock Price are interchangeable words, although stock price in the case is defined as avg of last 15 min trade.

2. For analysis, if ticker price is not provided, there is an option to use avg. stock price based of last 15min trades for analysis such as dividend yield, pe ratio.

3. In case no timestamp for a trade is provided, the timestamp is defaulted to current timestamp of trade entry. Assumption here is that its the latest trade execution.

4.In case of GBCE Index calculation, there is addition option where if no trades exists for last 15 mins of a particular ticker, the code looks for last 24hrs and if available, will use that for calculation. If both not available, it will request user input and accordingly include/exclude from index calclation. Here the assumption is stock price would not have moved significantly in a day although this may not necessarily hold true in practical scenario and 3-6hrs slot etc. can be experimented.

5.The code has been written keeping an end-user in the mind, who may or may not be from a programming background (for eg: analysts entering trade details or looking for key figures may not be from a programming background). Hence, a lot of print lines would be noticed that can guide the user. However, these can be suppressed depending on end-user.

6. There is no check in place to make sure that a ticker quantity sold is not greater than currently available, since it wasn't required in the realms of the case.

7. All entries for last dividend, par value will be assumed in pennies and fix dividend will be expected to be a percentage. Fixed dividend is a necessary requirement for preferred stock.

8. Expected timestamps for the trades is in the format YYYY-mm-dd HH:MM:SS.

Platform:
This code has been written to be run on a Linux platform with python 3.6.4 installed. All files should be place in the same directory and the the main module to run is ssstock_main.py

What to Expect:
The code systematically provides various options from stock_analysis to data_entry to index calculation, based of the assumptions specified above. However, one can avoid going through the options and call specific functions from the command line/console to investigate/test a particular functionality.

While various checks have been palced and rigorously tested for data integrity and delivery, the list may not have been exhaustive. 

pylint score = ~7/10 for both files.
