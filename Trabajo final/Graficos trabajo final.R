
require("ggplot2")
require("tibble")
require("dplyr")
require("Lock5Data")

#Creamos un nuevo data frame que considere solo los países africanos.

new_df <- subset(rugged_data_1_ , cont_africa != 0)
new_df

#Gráficos solo para África

#Gráfico que muestra la relación entre la rugosidad y el PBI per cápita en el año 2000 para los países africanos.
ggplot(new_df, aes(x=rugged, y=rgdppc_2000)) + geom_point(size=2) + geom_smooth(method=lm, se= FALSE, color="black")+
  labs(x="Rugosidad", y = "PBI per cápita año 2000")+ 
  theme_classic()

#Gráfico que muestra la relación entre la exportación de esclavos y el PBI per cápita del año 2000. Además, el color de los puntos denota el nivel de rugosidad del terreno. 
ggplot(new_df, aes(x=slave_exports, y=rgdppc_2000, color=rugged)) + geom_point(size=2) + xlim(0,200000) + geom_smooth(method=lm, se= FALSE, color="black")+
  labs(x="Exportación de esclavos", y = "PBI per cápita año 2000", color = "Rugosidad")+ 
  theme_classic()

#Gráfico que muestra la relación entre la exportación de esclavos y la rugosidad del terreno.
ggplot(new_df, aes(x=slave_exports, y=rugged)) + geom_point(size=2) +xlim(0,200000)+ geom_smooth(method=lm, se= FALSE, color="black")+
  labs(x="Exportación de esclavos", y = "Rugosidad")+ 
  theme_classic()

#Gráfico que muestra la relación entre la exportación de esclavos y la fertilidad de la tierra
ggplot(new_df, aes(x=slave_exports, y=soil)) + geom_point(size=2) + geom_smooth(method=lm, se= FALSE, color="black")+
  labs(x="Exportación de esclavos", y = "Fertilidad de la tierra")+ 
  theme_classic()



#Creamos un nuevo data frame que solo tenga en cuenta países no africanos.

new_df1 <- subset(rugged_data_1_ , cont_africa != 1)
new_df1

#Gráfico que muestra la relación entre la rugosidad y el PBI per cápita en el año 2000 para los países de la muestra que no estan en África.
ggplot(new_df1, aes(x=rugged, y=rgdppc_2000)) + geom_point(size=2) + xlim(0,6) + geom_smooth(method=lm, se= FALSE, color="black")+
  labs(x="Rugosidad", y = "PBI per cápita año 2000")+ 
  theme_classic()






