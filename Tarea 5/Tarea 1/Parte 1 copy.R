#Prior to use, install the following packages:
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

#Load the data files
df <- read.csv("data/gapminder-data.csv")
df2 <- read.csv("data/xAPI-Edu-Data.csv")
df3 <- read.csv("data/LoanStats.csv")

#Summary of the three datasets
str(df)
str(df2)
str(df3)

###GRAFICO 1
##Grammar of graphics and visual components
#Subtopic - Layers, color
p1 <- ggplot(df,aes(x=Electricity_consumption_per_capita))
p2 <- p1+geom_histogram(bins=15, color="black", fill="pink")
p2

#Exercise-Layers and background theme
p3 <- p2+xlab("Electricity consumption per capita")+ylab("Count")+  theme_calc()
p3

###GRAFICO 2

dfn <- subset(HollywoodMovies2013, Genre %in% c("Action","Adventure","Comedy","Drama","Romance")
              & LeadStudio %in% c("Fox","Sony","Columbia","Paramount","Disney"))
p1 <- ggplot(dfn,aes(Genre,WorldGross)) 
p1
p2 <- p1+geom_bar(stat="Identity",aes(fill=LeadStudio),position="dodge")
p2
p3 <- p2+theme(axis.title.x=element_text(size=15),
               axis.title.y=element_text(size=15),
               plot.background=element_rect(fill="white"),
               panel.background = element_rect(fill= "white"),
               panel.grid.major.x = element_blank() ,
               # explicitly set the horizontal lines (or they will disappear too)
               panel.grid.major.y = element_line( size=.1, color="grey" ) 
)
p3




###GRAFICO 3
### Exercise: Creating density plots
df3s <- subset(df3,grade %in% c("A","B","C","D","E","F","G"))

ggplot(df3s,aes(x=loan_amnt)) + geom_density() + facet_wrap(~grade) + 
  labs(x="Loan Amount", y="Density") + theme_calc() 



df3s <- subset(df3,grade %in% c("A","B","C","D","E","F","G"))

ggplot(df3s,aes(x=loan_amnt)) + geom_density(data = df3s, colour = "black") + 
  geom_density(aes(colour = grade))  +labs(y= "Density", x = "Loan Amount") 
options(scipen=5)

  
  
  
  