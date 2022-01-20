                                 PROJECT 1 "BICIMAD STATIONS"




MAIN OBJECTIVES
----------------

the main objectives with this project are:
- to get the closest bicimad station to an addres that we are introduccing in the powershell, in a csv file the program save this file in (Documents/IRONHACK_GITHUB/ih_datamadpt1121_project_m1/DATA/ubicacion_mas_cercana.csv).


- to get a table with all the bicimad stations and the distance to a determinate addres,the program save this file in (Documents/IRONHACK_GITHUB/ih_datamadpt1121_project_m1/DATA/todas_las_ubicaciones.csv). 

ENVIRONMENT
------------

We created a new environment called: proyecto1
In this environment we had to install the next libraries from python:
- python ( conda install python == 3.7  / pip install python == 3.7)
- Pandas (conda install pandas / pip install pandas)
- Numpy (conda install numpy / pip install numpy)
- Requests(conda install requests / pip install requests)
- Json (conda install json / pip install json)
- BeautifulSoup (conda install BeautifulSoup / pip install BeautifulSoup)
- Shapely.geometry (you dont have to install this library only import in your code file)
- Geopandas (conda install geopandas / pip install geopandas)
- Argparse (conda install argparse / pip install argparse)
- Sys (conda install sys / pip install sys)


IMPORTS IN YOUR CODE FILE
--------------------------

import pandas as pd 
import numpy as np
import requests
import json
from bs4 import BeautifulSoup 
from shapely.geometry import Point
import geopandas as gpd 
import argparse  #libreria para leer parametros de entrada en el terminal.
import sys



STARTING WITH THE CODE
------------------------


-First of all we imported all the databases we needed for the project: bicimad_stations( from sql, with Azure Data Studio) and Sedes.Centros con espacios deporticos( from the API Rest Portal de datos abiertos del Ayuntamiento de Madrid)

and after this we converted the databases in a pandas DataFrames to clean the data.

-Second of all we had to clean this two DataFrames because we didnt need all the columns of the Pandas DataFrames and we had to separate the columnn where we had latitude and longitude in two different columns in both DataFrames.


-The next step was to get a point between latitude and longitude because after this point we merged both dataframes and applied the functions To_mercator and distance_meters

to_mercator = we only used this function to get a point between latitude and longitude.
distance_meters = we used this function to get the distance between two different address/points.


-After all this steps we need a Dataframe with the closest bicimad station, so thats why we use the function: bicimad_mas_cercana().

we also need all the bicimad stations from a specific address so thats why we are using the function: todas_las_estaciones().


-The first and last point as we can see at the very top and bottom is to def argparse function(), we use this function because the customer have to introduce a parameter in the powershell (MasCercana, TodasEstaciones or nothing), so we hace to define some parameters.

If the customer dont introduce nothing -- the program get by default a csv file with the closest bicimad station (ubicacion_mas_cercana.csv)

If the customer dont know the parameters to introduce in the powershell, can use:

python main.py --help (and the program will give all the options to introduce in the powershell)



WHERE THE PROGRAM SAVE THE CSV FILES?
--------------------------------------

- Documents/IRONHACK_GITHUB/ih_datamadpt1121_project_m1/DATA/ubicacion_mas_cercana.csv
- Documents/IRONHACK_GITHUB/ih_datamadpt1121_project_m1/DATA/todas_ubicaciones.csv



--------------------------------------------------------------------------------------------
## **Project Main Stack**

- [Azure SQL Database](https://portal.azure.com/)

- [SQL Alchemy](https://docs.sqlalchemy.org/en/13/intro.html) (alternatively you can use _Azure Data Studio_)

- [Requests](https://requests.readthedocs.io/)

- [Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/index.html)

- Module `geo_calculations.py`

- [Argparse](https://docs.python.org/3.7/library/argparse.html)












 


 

