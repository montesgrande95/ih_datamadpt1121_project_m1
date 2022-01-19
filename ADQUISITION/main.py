import pandas as pd 
import numpy as np
import requests
import json
from bs4 import BeautifulSoup 
from shapely.geometry import Point
import geopandas as gpd 
import argparse  #libreria para leer parametros de entrada en el terminal.
import sys


"""

importamos la libreria de argparse,
parser = transforma el imput del usuario en una variable,
parser.add_argument( 
    metemos los argumentos que queremos.
    --tipo = para que el usuario meta el tipo de ejecucion que quiere,
    dest = "tipo" nombre de la variable dentro del codigo, al nombrarla dentro del if ponemos .tipo porque 
    es el nombre que le hemos dado a la varibale.
    default = es opcional y sirve para que si el usuario no mete nada me guarde un archivo con la 
    estacion mas cercana
    help = lo que nos hace es describirnos la variable, si no lo ponemos no pasaria nada, pero es para 
    que sepa que es la variable la persona que revisa el codigo.
)

"""

parser = argparse.ArgumentParser()
parser.add_argument(
    "--tipo",
    dest = "tipo",
    default = "MasCercana",
    help = "parametro para selecionar el tipo de ejecucion. Posibles valores: MasCercana , TodasEstaciones"
)

args = parser.parse_args(sys.argv[1:])


#FUNCION PARA OBTENER EL PUNTO ENTRE LATITUD Y LONGITUD

def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

#FUNCION PARA CALCULAR LA DISTANCIA TOTAL ENTRE LOS PUNTOS DE LOS DOS DATAFRAMES( ESTACIONES BICIMAD Y SEDES, ESPACIOS DEPORTIVOS)


def distance_meters(DISTANCIA_SEDES, DISTANCIA_BICIS):
    # return the distance in metres between to latitude/longitude pair point in degrees (i.e.: 40.392436 / -3.6994487)
    
    return DISTANCIA_SEDES.distance(DISTANCIA_BICIS)

#FUNCION PARA OBTENER LA ESTACION DE BICIMAD MAS CERCANA A UNA DE LAS DIRECCIONES DEL DATAFRAME SEDES.ESPACIOS DEPORTIVOS.

def bicimad_mas_cercana():
    i = str(input("Introduzca lugar para calcular la estacion de bicimad mas cercana: "))
    a = dataframe_total2[dataframe_total2["NOMBRE"] == i]
    return a.sort_values(by = "DISTANCIA TOTAL", ascending = True).head(1)


#FUNCION PARA QUE NOS SAQUE TODAS LAS ESTACIONES QUE TENEMOS CERCA DE UNA DIRECCION DETERMINADA.

def todas_las_estaciones():
    i = str(input("Introduzca lugar para obtener todas las estaciones de bicimad cercanas a la direccion dada: "))
    a = dataframe_total2[dataframe_total2["NOMBRE"] == i]
    return a.sort_values(by = "DISTANCIA TOTAL", ascending = True)


#CARGAR TABLA DE ESTACIONES DE BICIMAD
print("cargando tablas estaciones de bicimad")
dataframe_bicimadstations = pd.read_json("../DATA/bicimad_stations.json") 
print(dataframe_bicimadstations.head())
#CARGAR TABLA DE SEDES Y CENTROS DEPORTIVOS

print("cargando tablas de sedes y centros deportivos")
dataframe_centrosdeportivos = pd.read_csv("../DATA/212808-0-espacio-deporte.csv", delimiter = ";")
print(dataframe_centrosdeportivos.head())


#SEPARAMOS LAS COLUMNAS DE LATITUD Y LONGITUD EN DOS COLUMNAS DIFERENTES


dataframe_bicimadstations['LONGITUD'] = [float(index.split(',')[0].replace("[", "")) for index in dataframe_bicimadstations['geometry_coordinates']]
dataframe_bicimadstations['LATITUD'] = [float(index.split(',')[1].replace("]", "")) for index in dataframe_bicimadstations['geometry_coordinates']]



#NOS VAMOS A QUEDAR SOLO CON LAS COLUMNAS QUE NOS INTERESAN DE LA TABLA DE ESTACIONES DE BICIMAD
#Y APLICAMOS LAMBDA PARA QUE NOS CREE OTRA COLUMNA EN LA QUE NOS SALGA EL PUNT0 ENTRE LA LATITUD Y LA LONGITUD.

dataframe_bicis = pd.DataFrame(dataframe_bicimadstations[["name","address","LATITUD","LONGITUD"]])

print("calculando el punto entre la latitud y la longitud del dataframe estaciones de bicimad")
dataframe_bicis["DISTANCIA_BICIS"] = dataframe_bicis.apply(lambda x : to_mercator(x["LATITUD"],x["LONGITUD"]),axis=1)
print(dataframe_bicis.head())


#SOBRE LA SEGUNDA TABLA(TABLA DE SEDES ME QUEDO SOLO CON LAS COLUMNAS QUE ME INTERESAN).
#Y APLICAMOS LAMBDA PARA OBTENER EL PUNTO ENTRE LA LATITUD Y LA LONGITUD.

dataframe_sedes = pd.DataFrame(dataframe_centrosdeportivos[["NOMBRE" , "NOMBRE-VIA" , "DISTRITO" , "LATITUD" , "LONGITUD"]] )

print("calculando el punto entre la latitud y la longitud de sedes y espacios deportivos")
dataframe_sedes["DISTANCIA_SEDES"] = dataframe_sedes.apply(lambda x : to_mercator(x["LATITUD"],x["LONGITUD"]),axis=1)
print(dataframe_sedes.head())


#HACEMOS UN MERGE ENTRE LAS DOS TABLAS PARA QUE NOS SAQUE TODAS LAS COMBINACIONES POSIBLES ENTRE LAS DIRECCIONES.
#METEMOS UNA NUEVA COLUMNA CON EL TIPO DE LUGAR DE SEDES, ESPACIOS DEPORTIVOS.
print("haciendo el merge entre los dos dataframes")
dataframe_total = pd.merge(dataframe_sedes,dataframe_bicis, how = "cross")
dataframe_total["TIPO DE LUGAR"] = "SEDES. Centros con espacios deportivos"



#SELECCIONAMOS LAS COLUMNAS PRINCIPALES DEL DATAFRAME FINAL.
print("calculando un dataframe final con las columnas que me interesan entre las dos tablas")
dataframe_total2 = dataframe_total[["NOMBRE","NOMBRE-VIA","TIPO DE LUGAR","DISTRITO","DISTANCIA_SEDES","name","address","DISTANCIA_BICIS"]]


#CON LA FUNCION LAMBDA SACAMOS LA DISTANCIA TOTAL ENTRE TODAS LAS COMBINACIONES POSIBLES DE DIRECCIONES


print("calculando la distancia total entre los dos puntos obtenidos de los dos datasets")
dataframe_total2["DISTANCIA TOTAL"] =  dataframe_total2.apply(lambda x: distance_meters(x["DISTANCIA_SEDES"],x["DISTANCIA_BICIS"]),axis=1 )


print(dataframe_total2.head())

if args.tipo == "MasCercana":
    ubicacion_mas_cercana = bicimad_mas_cercana()
    # print(ubicacion_mas_cercana)
    ubicacion_mas_cercana.to_csv("../DATA/ubicacion_mas_cercana.csv", sep= ";")
    print("archivo estacion mas cercana guardado en la carpeta de DATA")

elif args.tipo == "TodasEstaciones":
    todas_ubicaciones = todas_las_estaciones()
    # print(distancias_ubicacion)
    todas_ubicaciones.to_csv("../DATA/todas_las_ubicaciones.csv", sep= ";")
    print("archivo de todas las estaciones guardado en la carpeta de DATA")

else:
    print("opcion erronea, solo podemos meter: MasCercana o TodasEstaciones")









