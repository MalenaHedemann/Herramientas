# Source: https://github.com/Robinlovelace/Creating-maps-in-R

x <- c("ggmap", "rgdal", "rgeos", "maptools", "dplyr", "tidyr", "tmap")

# warning: uncommenting this may take a number of minutes
install.packages(x) 
lapply(x, library, character.only = TRUE) # load the required packages

setwd("~/Google Drive/videos 2 y 3/")

library(rgdal)
lnd <- readOGR(dsn = "data/london_sport.shp")
# lnd <- readOGR(dsn = "data", layer = "london_sport")

library(rgeos)
library(rgdal)

crime_data <- read.csv("data/mps-recordedcrime-borough.csv",
                       stringsAsFactors = FALSE)

head(crime_data$CrimeType) # information about crime type

# Extract "Theft & Handling" crimes and save
crime_theft <- crime_data[crime_data$CrimeType == "Theft & Handling", ]

# Load dplyr package
library(dplyr)

# We use left_join because we want the length of the data frame to remain unchanged, with variables from new data appended in new columns (see ?left_join). The *join commands (including inner_join and anti_join) assume, by default, that matching variables have the same name. Here we will specify the association between variables in the two data sets:

head(lnd$name,100) # dataset to add to 
head(crime_ag$Borough,100) # the variables to join

head(left_join(lnd@data, crime_ag)) # you will need "by"
lnd@data <- left_join(lnd@data, crime_ag, by = c('name' = 'Borough'))

# tmap was created to overcome some of the limitations of base graphics and ggmap.
library(tmap) # load tmap package 
qtm(lnd, "CrimeCount") # plot the basic map
qtm(shp = lnd, fill = "Partic_Per", fill.palette = "Reds", fill.title = "Participation") 

## ggmap is based on the ggplot2 package, an implementation of the Grammar of Graphics (Wilkinson 2005). ggplot2 can replace the base graphics in R (the functions you have been plotting with so far). It contains default options that match good visualisation practice and is well-documented: http://docs.ggplot2.org/current/ .

#As a first attempt with ggplot2 we can create a scatter plot with the attribute data in the lnd object created previously:

library(ggplot2)
p <- ggplot(lnd@data, aes(Partic_Per, Pop_2001))

p + geom_point(aes(colour = Partic_Per, size = Pop_2001)) +
  geom_text(size = 2, aes(label = name))

install.packages("broom")
## ggmap requires spatial data to be supplied as data.frame, using tidy(). The generic plot() function can use Spatial objects directly; ggplot2 cannot. Therefore we need to extract them as a data frame. The tidy function was written specifically for this purpose. For this to work, broom package must be installed.
lnd_f <- broom::tidy(lnd)

# This step has lost the attribute information associated with the lnd object. We can add it back using the left_join function from the dplyr package (see ?left_join).
lnd$id <- row.names(lnd) # allocate an id variable to the sp data
head(lnd@data, n = 2) # final check before join (requires shared variable name)
lnd_f <- left_join(lnd_f, lnd@data) # join the data

# The new lnd_f object contains coordinates alongside the attribute information associated with each London Borough. It is now straightforward to produce a map with ggplot2. coord_equal() is the equivalent of asp = T in regular plots with R:

## ----"Map of Lond Sports Participation"-------------------------------
map <- ggplot(lnd_f, aes(long, lat, group = group, fill = Partic_Per)) +
  geom_polygon() + coord_equal() +
  labs(x = "Easting (m)", y = "Northing (m)",
       fill = "% Sports\nParticipation") +
  ggtitle("London Sports Participation")
map + scale_fill_gradient(low = "white", high = "black")
map