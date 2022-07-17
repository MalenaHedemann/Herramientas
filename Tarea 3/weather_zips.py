#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 15:04:21 2022

@author: malenahedemann
"""

#Instalar en python: 
#pip install wwo-hist

#### Import package

from wwo_hist import retrieve_hist_data


#### Set working directory to store output csv file(s)
import os
os.chdir("/Users/malenahedemann/Desktop/Clases herramientas/Clase 3/Tarea/Weather")


frequency=24
start_date = '01-JAN-2015'
end_date = '31-DEC-2015'
api_key = '535a0388efce401796922753220807'
location_list = ['20601','20607','20615','20619','20724','20759','20812','21001','21074','21087','21502','21601','21607',
'21613','21629','21651','21702','21713','21804','21811','21817','21901','21201','21520']

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)


