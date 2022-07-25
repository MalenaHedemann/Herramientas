Prior to use, install the following packages:
  install.packages("ggplot2")
install.packages("tibble")
install.packages("dplyr")
install.packages("gridExtra")
install.packages("Lock5Data")
install.packages("ggthemes")

install.packages("maps")
install.packages("mapproj")
install.packages("corrplot")
install.packages("fun")
install.packages("zoo")

#Load Libraries
library("ggplot2")
library("tibble")
library("gridExtra")
library("dplyr")
library("Lock5Data")
library("ggthemes")
library("fun")
library("zoo")
library("corrplot")
library("maps")
library("mapproj")

#Set pathname for the directory where you have data
setwd("~/MAESTRIA/Herramientas/Clase 6/Applied-Data-Visualization-with-R-and-ggplot2-master")
#Check working directory
getwd()

#Note: Working directory should be "Beginning-Data-Visualization-with-ggplot2-and-R"

#Load the data files
df <- read.csv("data/gapminder-data.csv")
df2 <- read.csv("data/xAPI-Edu-Data.csv")
df3 <- read.csv("data/LoanStats.csv")

#Summary of the three datasets
str(df)
str(df2)
str(df3)

##Grammar of graphics and visual components
#Subtopic - Layers, color
p1 <- ggplot(df,aes(x=Electricity_consumption_per_capita))
p2 <- p1+geom_histogram(bins=15, color="black", fill="pink")
p2

#Exercise-Layers and background theme
p3 <- p2+xlab("Electricity consumption per capita")+ylab("Count")+  theme_calc()
p3
  


