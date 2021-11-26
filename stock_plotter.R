#this script reads in stock data and plots it
#install.packages("ggplot2")
#install.packages("plyr")
#install.packages("jpeg")
print("processing...")
require(plyr)
require(ggplot2)
require(png)

raw_data <- readLines("/home/michael/stock_project/stock_cache.txt")

date_list <- list()
price_list <- list()
stock_order <- c()
stock_count <- 0
list_index <- 1
for(i in 1:length(raw_data)){
  if(grepl("beginning_new_stock_here:", raw_data[i])){
    stock_count <- stock_count + 1
    date_list[[stock_count]] <- c("begin")
    price_list[[stock_count]] <- c("begin")
    stock_order[stock_count] <- raw_data[i]
    list_index <- 1
    #names(date_list) <- c(names(date_list), raw_data[i])
    #names(price_list) <- c(names(price_list), raw_data[i])
  }else{
    line_data <- strsplit(raw_data[i], "    ")[[1]]
    date_list[[stock_count]][list_index] <- line_data[1]
    price_list[[stock_count]][list_index] <- line_data[2]
    list_index <- list_index + 1
    #date_list[[stock_count]] <- c(date_list[[stock_count]], line_data[1])
    #price_list[[stock_count]] <- c(price_list[[stock_count]], line_data[2])
  }
}

row_counter <- 0
stock_vec <- c()
date_vec <- c()
price_vec <-c()
vectors_index <- 1

for(i in 1:stock_count){
  stock_name <- strsplit(stock_order[i], "beginning_new_stock_here:")[[1]][1]
  for(j in 1:length(date_list[[i]])){
    if(date_list[[i]][j] != "begin"){
      stock_vec[vectors_index] <- stock_name
      date_vec[vectors_index] <- date_list[[i]][j]
      price_vec[vectors_index] <- price_list[[i]][j]
      vectors_index <- vectors_index + 1
      #new_row <- data.frame(stock = stock_name, date = date_list[[i]][j], price = price_list[[i]][j])
      #combined_data <- rbind(combined_data, new_row) 
    }
  }
}
price_vec <- as.numeric(price_vec)
date_vec <- as.Date(date_vec)
combined_data <- data.frame(stock = stock_vec, date = date_vec, price = price_vec)
combined_data <- na.omit(combined_data)
step <- round_any(accuracy = 10, x = (max(combined_data$price / 25)))
if(step == 0){
  step <- 1
}
price_breaks <- seq(0, max(combined_data$price), step)


png("/home/michael/stock_project/stock_plot.png", width = 12, height = 8, units = "in", res = 150)
ggplot(combined_data, aes( x=date, y=price, group=stock, col=stock)) + 
  geom_line() + scale_x_date(name = 'Date', date_breaks = '5 years', date_labels = '%Y', limits = c(min(combined_data$date), max(combined_data$date))) +
  scale_y_continuous(name = "Closing Price", breaks=price_breaks, labels = price_breaks)
dev.off()
cat("done!")  
