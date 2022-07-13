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
location_list = ['20637', '20653', '20688', '20740', '20871', '21040', '21043', 
                 '21158', '21220', '21240', '21502', '21601', '21638', '21639',
                 '21643', '21651', '21709', '21742', '21801', '21811', '21853', 
                 '21902']

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)


