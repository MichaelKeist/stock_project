#this script reads in stock data and plots it
#install.packages("ggplot2")
#install.packages("plyr")
library(plyr)
library(ggplot2)
raw_data <- readLines("/home/michael/stock_project/stock_cache.txt")

date_list <- list()
price_list <- list()
stock_order <- c()
stock_count <- 0
for(i in 1:length(raw_data)){
  if(grepl("55392898", raw_data[i])){
    stock_count <- stock_count + 1
    date_list[[stock_count]] <- c("begin")
    price_list[[stock_count]] <- c("begin")
    stock_order[stock_count] <- raw_data[i]
    #names(date_list) <- c(names(date_list), raw_data[i])
    #names(price_list) <- c(names(price_list), raw_data[i])
  }else{
    line_data <- strsplit(raw_data[i], "    ")[[1]]
    date_list[[stock_count]] <- c(date_list[[stock_count]], line_data[1])
    price_list[[stock_count]] <- c(price_list[[stock_count]], line_data[2])
  }
}

row_counter <- 0
combined_data <- data.frame(stock = 0, date = 0, price = 0)

for(i in 1:stock_count){
  stock_name <- strsplit(stock_order[i], "55392898")[[1]][1]
  for(j in 1:length(date_list[[i]])){
    if(date_list[[i]][j] != "begin"){
      new_row <- data.frame(stock = stock_name, date = date_list[[i]][j], price = price_list[[i]][j])
      combined_data <- rbind(combined_data, new_row) 
    }
  }
}
combined_data <- combined_data[-1,]
combined_data$date <- as.Date(combined_data$date)
combined_data$price <- as.numeric(combined_data$price)
combined_data <- na.omit(combined_data)
price_breaks <- seq(0, max(combined_data$price), round_any(accuracy = 10, x = (max(combined_data$price / 25))))
#as.character(seq(0, max(combined_data$price), 10))

ggplot(combined_data, aes( x=date, y=price, group=stock, col=stock)) + 
  geom_line() + scale_x_date(name = 'Date', date_breaks = '5 years', date_labels = '%Y', limits = c(min(combined_data$date), max(combined_data$date))) +
  scale_y_continuous(name = "Closing Price", breaks=price_breaks, labels = price_breaks)
  
