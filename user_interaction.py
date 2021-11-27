#This script interacts with the user and passes their input to R for visualization
import pandas as pd
import yfinance as yf
import sys
import csv
import requests
from io import StringIO
import html5lib
from bs4 import BeautifulSoup
#from selenium import webdriver
#from BeautifulSoup import BeautifulSoup
#from get_all_tickers import get_tickers as gt
#all_tickers = gt.get_tickers()
def generate_output(stocks):
    stocks = list(stocks)
    print("fetching data...")
    output_dict = {}
    cache_file = open("/home/michael/stock_project/stock_cache.txt", "a")
    for stock in stocks:
        current_data = yf.Ticker(stock)
        current_data = current_data.history(period = "max")
        output_dict[stock] = current_data
    for stock in output_dict:
        closing_prices = output_dict[stock]["Close"]
        frame_string = closing_prices.to_string()
        frame_string = stock + "beginning_new_stock_here:" + frame_string
        cache_file.write(frame_string + "\n")
    cache_file.close()


def sector():
    print("Finding stocks by sector")
    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    stocks_by_weight1 = pd.read_html("https://fknol.com/list/market-cap-sp-500-index-companies.php")[0].iloc(1)[0][2:]
    stocks_by_weight2 = pd.read_html("https://fknol.com/list/market-cap-sp-500-index-companies.php?go=a100")[0].iloc(1)[0][2:]
    stocks_by_weight3 = pd.read_html("https://fknol.com/list/market-cap-sp-500-index-companies.php?go=a200")[0].iloc(1)[0][2:]
    stocks_by_weight4 = pd.read_html("https://fknol.com/list/market-cap-sp-500-index-companies.php?go=a300")[0].iloc(1)[0][2:]
    stocks_by_weight5 = pd.read_html("https://fknol.com/list/market-cap-sp-500-index-companies.php?go=a400")[0].iloc(1)[0][2:]
    stocks_by_weight6 = pd.read_html("https://fknol.com/list/market-cap-sp-500-index-companies.php?go=a500")[0].iloc(1)[0][2:]
    frames = [stocks_by_weight1, stocks_by_weight2, stocks_by_weight3, stocks_by_weight4, stocks_by_weight5, stocks_by_weight6]
    stocks_by_weight = pd.concat(frames)
    stocks_by_weight = stocks_by_weight.reset_index()["Company(Ticker)"]
    sectors = set(table["GICS Sector"])
    sector_ready = True
    while sector_ready:
        sector_command = input("Type a valid sector, listsectors, or done to exit: ").lower()
        if sector_command == "done":
            sector_ready = False
        elif sector_command == "listsectors":
            print(sectors)
        elif sector_command.title() in sectors:
            numstocks = int(input("Plot the top X companies in the sector:  "))
            sector_bool = table["GICS Sector"] == sector_command.title()
            #maybe try having the R script title the plot based on what sector we look at
            slim_stocks = set(table[sector_bool]["Symbol"])
            if numstocks > len(slim_stocks):
                print("Too many stocks selected")
                numstocks = len(slim_stocks)
                selected_stocks = list(slim_stocks)
            else:
                selected_stocks = set()
                counter = 0
                while len(selected_stocks) < numstocks:
                    current_stock = stocks_by_weight.loc[counter].split("(")[1].split(")")[0]
                    if current_stock in slim_stocks:
                        selected_stocks.add(current_stock)
                    counter += 1
            generate_output(selected_stocks)


def main():
    print("Enter one of the following commands.")
    print("quit, stocks, bysector")
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
                    cache_file = open("/home/michael/stock_project/stock_cache.txt", "a")
                    print("fetching data...")
                    getting_stocks = False
                elif True:
                    current_stock = current_stock.upper()
                    stock_set.add(current_stock)
            for stock in stock_set:
                current_data = yf.Ticker(stock)
                current_data = current_data.history(period = "max")
                output_dict[stock] = current_data
            for stock in output_dict:
                #data_set = output_dict[stock]
                closing_prices = output_dict[stock]["Close"]
                frame_string = closing_prices.to_string()
                frame_string = stock + "beginning_new_stock_here:" + frame_string
                cache_file.write(frame_string + "\n")
            cache_file.close()
        elif current_command == "bysector":
            sector()
#existence of 55392898 identifies the first line of new stock
main()
