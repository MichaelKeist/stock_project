#This script interacts with the user and passes their input to R for visualization
import yfinance as yf
import sys
import csv
from io import StringIO
#from get_all_tickers import get_tickers as gt
#all_tickers = gt.get_tickers()

def main():
    print("Enter one of the following commands.")
    print("quit, stocks")
    user_ready = True
    while user_ready:
        current_command = input("Please enter a command: ").lower()
        if current_command == "quit":
            user_ready = False
            print("Exiting")
        elif current_command == "stocks":
            getting_stocks = True
            output_dict = {}
            stock_set = set()
            while getting_stocks:
                current_stock = input("Enter a stock symbol, or done to stop: ").lower()
                if current_stock == "done":
                    getting_stocks = False
                elif True:
                    current_stock = current_stock.upper()
                    stock_set.add(current_stock)
            for stock in stock_set:
                current_data = yf.Ticker(stock)
                current_data = current_data.history(period = "max")
                output_dict[stock] = current_data
            output_string = ""
            for stock in output_dict:
                #data_set = output_dict[stock]
                closing_prices = output_dict[stock]["Close"]
                frame_string = closing_prices.to_string()
                frame_string = stock + "55392898" + frame_string
                output_string = output_string + frame_string + "\n"
            cache_file = open("stock_cache.txt", "w")
            cache_file.write(output_string)
            cache_file.close()
#existence of 55392898 identifies the first line of new stock
main()
